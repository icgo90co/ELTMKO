"""
MySQL Loader Module
Handles connection and data loading to MySQL database
"""
import logging
import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)


class MySQLLoader:
    """Manages MySQL connections and data loading operations"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize MySQL loader
        
        Args:
            config: MySQL connection configuration
        """
        self.config = config
        self.connection = None
        
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.config.get('host'),
                port=self.config.get('port', 3306),
                user=self.config.get('user'),
                password=self.config.get('password'),
                database=self.config.get('database')
            )
            logger.info(f"Connected to MySQL database: {self.config.get('database')}")
        except Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            raise
    
    def disconnect(self):
        """Close MySQL connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("MySQL connection closed")
    
    def ensure_connection(self):
        """Ensure database connection is active"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
    
    def create_table_if_not_exists(self, table_name: str, schema: Dict[str, str]):
        """
        Create table if it doesn't exist
        
        Args:
            table_name: Name of the table
            schema: Dictionary mapping column names to SQL types
        """
        self.ensure_connection()
        
        columns = []
        for col_name, col_type in schema.items():
            columns.append(f"`{col_name}` {col_type}")
        
        columns_str = ", ".join(columns)
        
        # Add metadata columns
        create_query = f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            {columns_str},
            `_elt_loaded_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `_elt_updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_query)
            self.connection.commit()
            cursor.close()
            logger.info(f"Table '{table_name}' is ready")
        except Error as e:
            logger.error(f"Error creating table '{table_name}': {e}")
            raise
    
    def load_dataframe(self, df: pd.DataFrame, table_name: str, mode: str = 'append'):
        """
        Load pandas DataFrame into MySQL table
        
        Args:
            df: Pandas DataFrame to load
            table_name: Target table name
            mode: 'append' or 'replace'
        """
        if df.empty:
            logger.warning(f"DataFrame is empty, nothing to load to '{table_name}'")
            return
        
        self.ensure_connection()
        
        try:
            # Infer schema from DataFrame
            schema = self._infer_schema_from_dataframe(df)
            self.create_table_if_not_exists(table_name, schema)
            
            # Prepare data for insertion
            columns = list(df.columns)
            placeholders = ", ".join(["%s"] * len(columns))
            columns_str = ", ".join([f"`{col}`" for col in columns])
            
            if mode == 'replace':
                # Truncate table before loading
                cursor = self.connection.cursor()
                cursor.execute(f"TRUNCATE TABLE `{table_name}`")
                cursor.close()
            
            # Insert data
            insert_query = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({placeholders})"
            
            cursor = self.connection.cursor()
            
            # Convert DataFrame to list of tuples
            data = [tuple(row) for row in df.values]
            
            cursor.executemany(insert_query, data)
            self.connection.commit()
            
            rows_inserted = cursor.rowcount
            cursor.close()
            
            logger.info(f"Loaded {rows_inserted} rows into '{table_name}'")
            
        except Error as e:
            logger.error(f"Error loading data to '{table_name}': {e}")
            if self.connection:
                self.connection.rollback()
            raise
    
    def upsert_dataframe(self, df: pd.DataFrame, table_name: str, key_columns: List[str]):
        """
        Upsert DataFrame into MySQL table (INSERT ... ON DUPLICATE KEY UPDATE)
        
        Args:
            df: Pandas DataFrame to upsert
            table_name: Target table name
            key_columns: Columns to use as unique keys
        """
        if df.empty:
            logger.warning(f"DataFrame is empty, nothing to upsert to '{table_name}'")
            return
        
        self.ensure_connection()
        
        try:
            # Infer schema and create table
            schema = self._infer_schema_from_dataframe(df)
            
            # Add unique key constraint
            self.create_table_if_not_exists(table_name, schema)
            
            # Add missing columns to existing table
            self._add_missing_columns(table_name, schema)
            
            self._ensure_unique_key(table_name, key_columns)
            
            # Prepare upsert query
            columns = list(df.columns)
            columns_str = ", ".join([f"`{col}`" for col in columns])
            placeholders = ", ".join(["%s"] * len(columns))
            
            # Update clause for non-key columns
            update_columns = [col for col in columns if col not in key_columns]
            update_str = ", ".join([f"`{col}` = VALUES(`{col}`)" for col in update_columns])
            
            upsert_query = f"""
            INSERT INTO `{table_name}` ({columns_str})
            VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE {update_str}
            """
            
            cursor = self.connection.cursor()
            data = [tuple(row) for row in df.values]
            cursor.executemany(upsert_query, data)
            self.connection.commit()
            
            rows_affected = cursor.rowcount
            cursor.close()
            
            logger.info(f"Upserted {rows_affected} rows into '{table_name}'")
            
        except Error as e:
            logger.error(f"Error upserting data to '{table_name}': {e}")
            if self.connection:
                self.connection.rollback()
            raise
    
    def _ensure_unique_key(self, table_name: str, key_columns: List[str]):
        """
        Ensure unique key exists on the table
        
        Args:
            table_name: Table name
            key_columns: Columns for unique key
        """
        try:
            cursor = self.connection.cursor()
            key_name = f"uk_{'_'.join(key_columns)}"
            key_columns_str = ", ".join([f"`{col}`" for col in key_columns])
            
            # Check if key exists
            cursor.execute(f"""
                SELECT COUNT(*) FROM information_schema.statistics 
                WHERE table_schema = '{self.config.get('database')}' 
                AND table_name = '{table_name}' 
                AND index_name = '{key_name}'
            """)
            
            if cursor.fetchone()[0] == 0:
                # Create unique key
                alter_query = f"ALTER TABLE `{table_name}` ADD UNIQUE KEY `{key_name}` ({key_columns_str})"
                cursor.execute(alter_query)
                self.connection.commit()
                logger.info(f"Created unique key '{key_name}' on '{table_name}'")
            
            cursor.close()
        except Error as e:
            logger.warning(f"Could not ensure unique key on '{table_name}': {e}")
    
    def _add_missing_columns(self, table_name: str, schema: Dict[str, str]):
        """
        Add missing columns to existing table
        
        Args:
            table_name: Table name
            schema: Dictionary mapping column names to SQL types
        """
        try:
            cursor = self.connection.cursor()
            
            # Get existing columns
            cursor.execute(f"DESC `{table_name}`")
            existing_columns = {row[0] for row in cursor.fetchall()}
            
            # Find missing columns
            missing_columns = set(schema.keys()) - existing_columns
            
            # Add missing columns
            for col_name in missing_columns:
                col_type = schema[col_name]
                alter_query = f"ALTER TABLE `{table_name}` ADD COLUMN `{col_name}` {col_type}"
                
                try:
                    cursor.execute(alter_query)
                    self.connection.commit()
                    logger.info(f"Added column '{col_name}' to table '{table_name}'")
                except Error as e:
                    logger.warning(f"Could not add column '{col_name}' to '{table_name}': {e}")
            
            cursor.close()
        except Error as e:
            logger.warning(f"Could not check for missing columns on '{table_name}': {e}")
    
    def _infer_schema_from_dataframe(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Infer MySQL schema from pandas DataFrame
        
        Args:
            df: Pandas DataFrame
            
        Returns:
            Dictionary mapping column names to SQL types
        """
        schema = {}
        
        for col in df.columns:
            dtype = df[col].dtype
            
            if pd.api.types.is_integer_dtype(dtype):
                schema[col] = "BIGINT"
            elif pd.api.types.is_float_dtype(dtype):
                schema[col] = "DOUBLE"
            elif pd.api.types.is_bool_dtype(dtype):
                schema[col] = "BOOLEAN"
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                schema[col] = "DATETIME"
            else:
                # Default to TEXT for strings and other types
                schema[col] = "TEXT"
        
        return schema
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results
        
        Args:
            query: SQL query to execute
            
        Returns:
            List of dictionaries representing rows
        """
        self.ensure_connection()
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            logger.error(f"Error executing query: {e}")
            raise
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
