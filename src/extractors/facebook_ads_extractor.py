"""
Facebook Ads Extractor
Extracts data from Facebook Ads API
"""
import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adsinsights import AdsInsights

logger = logging.getLogger(__name__)


class FacebookAdsExtractor:
    """Extracts data from Facebook Ads API"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Facebook Ads extractor
        
        Args:
            config: Facebook Ads API configuration
        """
        self.config = config
        self.api = None
        self.ad_account = None
        self._initialize_api()
    
    def _initialize_api(self):
        """Initialize Facebook Ads API"""
        try:
            app_id = self.config.get('app_id')
            app_secret = self.config.get('app_secret')
            access_token = self.config.get('access_token')
            
            # Initialize API with latest version (v22.0)
            FacebookAdsApi.init(app_id, app_secret, access_token, api_version='v22.0')
            self.api = FacebookAdsApi.get_default_api()
            
            ad_account_id = self.config.get('ad_account_id')
            self.ad_account = AdAccount(ad_account_id)
            
            logger.info(f"Facebook Ads API initialized for account: {ad_account_id}")
            
        except Exception as e:
            logger.error(f"Error initializing Facebook Ads API: {e}")
            raise
    
    def _expand_action_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Expand complex action fields (actions, cost_per_action_type, video_play_actions, etc.)
        into individual columns
        
        Args:
            df: DataFrame with JSON string columns
            
        Returns:
            DataFrame with expanded action columns
        """
        # Common action types to extract
        action_types_to_extract = [
            'lead',  # Formularios de leads
            'landing_page_view',  # Vistas de página de destino
            'link_click',  # Clics en enlaces
            'post_engagement',  # Interacciones con publicación
            'page_engagement',  # Interacciones con página
            'purchase',  # Compras
            'add_to_cart',  # Agregar al carrito
            'initiate_checkout',  # Iniciar pago
            'complete_registration',  # Registro completado
            'submit_application',  # Envío de solicitud
            'schedule',  # Programaciones
            'contact',  # Contactos
            'customize_product',  # Personalizar producto
            'donate',  # Donaciones
            'find_location',  # Encontrar ubicación
            'start_trial',  # Iniciar prueba
            'subscribe',  # Suscripciones
            'search',  # Búsquedas
        ]
        
        # Fields to expand
        fields_to_expand = {
            'actions': 'action',  # Generates: action_lead, action_purchase, etc.
            'cost_per_action_type': 'cost_per',  # Generates: cost_per_lead, cost_per_purchase, etc.
            'video_play_actions': 'video',  # Generates: video_play, video_view, etc.
        }
        
        for field_name, prefix in fields_to_expand.items():
            if field_name not in df.columns:
                continue
            
            logger.info(f"Expanding field: {field_name}")
            
            # Extract and expand
            for idx, row_value in df[field_name].items():
                if pd.isna(row_value) or not row_value:
                    continue
                
                try:
                    # Parse JSON string
                    if isinstance(row_value, str):
                        actions_list = json.loads(row_value)
                    elif isinstance(row_value, list):
                        actions_list = row_value
                    else:
                        continue
                    
                    # Extract each action type
                    for action in actions_list:
                        if not isinstance(action, dict):
                            continue
                        
                        action_type = action.get('action_type', '')
                        action_value = action.get('value', 0)
                        
                        # Create column name
                        col_name = f"{prefix}_{action_type}"
                        
                        # Initialize column if it doesn't exist
                        if col_name not in df.columns:
                            df[col_name] = None
                        
                        # Set value
                        df.at[idx, col_name] = action_value
                        
                except Exception as e:
                    logger.debug(f"Error expanding {field_name} at row {idx}: {e}")
                    continue
        
        return df
    
    def extract_campaigns(self, fields: List[str] = None) -> pd.DataFrame:
        """
        Extract campaigns from Facebook Ads
        
        Args:
            fields: List of fields to extract
            
        Returns:
            DataFrame with campaigns data
        """
        if fields is None:
            fields = [
                Campaign.Field.id,
                Campaign.Field.name,
                Campaign.Field.status,
                Campaign.Field.objective,
                Campaign.Field.created_time,
                Campaign.Field.updated_time,
            ]
        
        try:
            logger.info("Extracting campaigns from Facebook Ads...")
            campaigns = self.ad_account.get_campaigns(fields=fields)
            
            data = []
            for campaign in campaigns:
                data.append(dict(campaign))
            
            df = pd.DataFrame(data)
            logger.info(f"Extracted {len(df)} campaigns")
            
            return df
            
        except Exception as e:
            logger.error(f"Error extracting campaigns: {e}")
            raise
    
    def extract_adsets(self, fields: List[str] = None) -> pd.DataFrame:
        """
        Extract ad sets from Facebook Ads
        
        Args:
            fields: List of fields to extract
            
        Returns:
            DataFrame with ad sets data
        """
        if fields is None:
            fields = [
                AdSet.Field.id,
                AdSet.Field.name,
                AdSet.Field.status,
                AdSet.Field.campaign_id,
                AdSet.Field.daily_budget,
                AdSet.Field.lifetime_budget,
                AdSet.Field.created_time,
                AdSet.Field.updated_time,
            ]
        
        try:
            logger.info("Extracting ad sets from Facebook Ads...")
            adsets = self.ad_account.get_ad_sets(fields=fields)
            
            data = []
            for adset in adsets:
                data.append(dict(adset))
            
            df = pd.DataFrame(data)
            logger.info(f"Extracted {len(df)} ad sets")
            
            return df
            
        except Exception as e:
            logger.error(f"Error extracting ad sets: {e}")
            raise
    
    def extract_ads(self, fields: List[str] = None) -> pd.DataFrame:
        """
        Extract ads from Facebook Ads
        
        Args:
            fields: List of fields to extract
            
        Returns:
            DataFrame with ads data
        """
        if fields is None:
            fields = [
                Ad.Field.id,
                Ad.Field.name,
                Ad.Field.status,
                Ad.Field.adset_id,
            ]
        
        try:
            logger.info("Extracting ads from Facebook Ads...")
            ads = self.ad_account.get_ads(fields=fields)
            
            data = []
            for ad in ads:
                ad_dict = dict(ad)
                # Remove complex objects that can't be stored in MySQL
                ad_dict.pop('creative', None)
                data.append(ad_dict)
            
            df = pd.DataFrame(data)
            logger.info(f"Extracted {len(df)} ads")
            
            return df
            
        except Exception as e:
            logger.error(f"Error extracting ads: {e}")
            raise
    
    def extract_insights(
        self,
        level: str = 'account',
        date_range: int = None,
        start_date: str = None,
        end_date: str = None,
        time_increment: str = 'daily',
        fields: List[str] = None
    ) -> pd.DataFrame:
        """
        Extract insights (metrics) from Facebook Ads
        
        Args:
            level: Aggregation level ('account', 'campaign', 'adset', 'ad')
            date_range: Number of days to look back (alternative to start_date/end_date)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            time_increment: 'daily' (1) or 'monthly' (all_days)
            fields: List of fields to extract
            
        Returns:
            DataFrame with insights data
        """
        if fields is None:
            fields = [
                AdsInsights.Field.date_start,
                AdsInsights.Field.date_stop,
                AdsInsights.Field.impressions,
                AdsInsights.Field.clicks,
                AdsInsights.Field.spend,
                AdsInsights.Field.reach,
                AdsInsights.Field.ctr,
                AdsInsights.Field.cpc,
                AdsInsights.Field.cpm,
                AdsInsights.Field.frequency,
            ]
        
        # Add ID fields based on level
        if level == 'campaign':
            fields.append(AdsInsights.Field.campaign_id)
            fields.append(AdsInsights.Field.campaign_name)
        elif level == 'adset':
            fields.append(AdsInsights.Field.campaign_id)
            fields.append(AdsInsights.Field.adset_id)
            fields.append(AdsInsights.Field.adset_name)
        elif level == 'ad':
            fields.append(AdsInsights.Field.campaign_id)
            fields.append(AdsInsights.Field.adset_id)
            fields.append(AdsInsights.Field.ad_id)
            fields.append(AdsInsights.Field.ad_name)
        
        # Calculate date range
        if start_date is None or end_date is None:
            date_range = date_range or 30
            end_dt = datetime.now().date()
            start_dt = end_dt - timedelta(days=date_range)
        else:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Map time_increment to Facebook API values
        # 1 = one row per day
        # 'monthly' = one row per month (but Facebook uses special format)
        # 'all_days' = one row for entire period
        if time_increment == 'daily':
            time_increment_value = 1
        elif time_increment == 'monthly':
            # Facebook agrupa por mes cuando usas 'monthly' pero devuelve date_start como primer día del mes
            time_increment_value = 'monthly'
        else:
            # Sin breakdown - un solo registro para todo el período
            time_increment_value = 'all_days'
        
        params = {
            'level': level,
            'time_range': {
                'since': start_dt.strftime('%Y-%m-%d'),
                'until': end_dt.strftime('%Y-%m-%d')
            },
            'time_increment': time_increment_value,
        }
        
        try:
            logger.info(f"Extracting insights from Facebook Ads...")
            logger.info(f"  Level: {level}")
            logger.info(f"  Date range: {start_dt} to {end_dt} ({(end_dt - start_dt).days + 1} days)")
            logger.info(f"  Time increment: {time_increment_value}")
            logger.info(f"  Fields: {len(fields)} metrics")
            
            insights = self.ad_account.get_insights(fields=fields, params=params)
            
            # Debug: contar resultados
            insights_list = list(insights)
            logger.info(f"  Facebook API returned {len(insights_list)} raw records")
            
            if not insights_list:
                logger.warning("No data returned from Facebook API")
                return pd.DataFrame()
            
            data = []
            all_keys = set()  # Track all unique keys
            
            # First pass: collect all insights and identify all keys
            for insight in insights_list:
                insight_dict = dict(insight)
                
                # Clean up complex types (lists, dicts) - convert to JSON strings
                # Also remove any None values that might cause issues
                cleaned_dict = {}
                for key, value in insight_dict.items():
                    # Skip None values and invalid column names
                    if value is None or key is None or str(key).lower() == 'nan':
                        continue
                    
                    if isinstance(value, (list, dict)):
                        # Convert complex types to JSON string
                        try:
                            cleaned_dict[key] = json.dumps(value)
                        except:
                            cleaned_dict[key] = str(value)
                    else:
                        cleaned_dict[key] = value
                
                if cleaned_dict:  # Only add if there are valid fields
                    data.append(cleaned_dict)
                    all_keys.update(cleaned_dict.keys())
            
            if not data:
                logger.warning("No valid data extracted from insights")
                return pd.DataFrame()
            
            # Second pass: normalize all dicts to have the same keys (fill missing with None)
            normalized_data = []
            for record in data:
                normalized_record = {}
                for key in all_keys:
                    normalized_record[key] = record.get(key, None)
                normalized_data.append(normalized_record)
            
            df = pd.DataFrame(normalized_data)
            
            # Expand complex action fields BEFORE cleaning
            df = self._expand_action_fields(df)
            
            # Final cleanup: Remove any NaN column names and invalid names
            # First remove columns where the name itself is NaN/None
            df = df.loc[:, ~df.columns.isna()]
            
            # Then filter out columns with invalid string names
            invalid_names = {'nan', 'none', 'nat', 'null', 'undefined'}
            valid_columns = [
                col for col in df.columns 
                if str(col).strip().lower() not in invalid_names
            ]
            df = df[valid_columns]
            
            logger.info(f"DataFrame columns after cleaning: {list(df.columns)}")
            
            # Convert numeric columns
            numeric_columns = ['impressions', 'clicks', 'spend', 'reach', 'frequency']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Convert percentage columns
            percentage_columns = ['ctr', 'cpc', 'cpm']
            for col in percentage_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Convert date columns
            if 'date_start' in df.columns:
                df['date_start'] = pd.to_datetime(df['date_start'])
            if 'date_stop' in df.columns:
                df['date_stop'] = pd.to_datetime(df['date_stop'])
            
            logger.info(f"Extracted {len(df)} insights records")
            logger.info(f"DataFrame columns from extractor: {list(df.columns)}")
            logger.info(f"DataFrame dtypes from extractor: {df.dtypes.to_dict()}")
            
            # Final check for 'nan' column
            if 'nan' in [str(col).lower() for col in df.columns]:
                logger.error(f"❌ FOUND 'nan' column in DataFrame! Columns: {list(df.columns)}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error extracting insights: {e}")
            raise
    
    def extract_table(self, table_config: Dict[str, Any]) -> pd.DataFrame:
        """
        Extract data based on table configuration
        
        Args:
            table_config: Table configuration from config file
            
        Returns:
            DataFrame with extracted data
        """
        table_name = table_config.get('name')
        fields = table_config.get('fields', [])
        
        if table_name == 'campaigns':
            return self.extract_campaigns(fields=fields if fields else None)
        elif table_name == 'adsets':
            return self.extract_adsets(fields=fields if fields else None)
        elif table_name == 'ads':
            return self.extract_ads(fields=fields if fields else None)
        elif table_name == 'insights':
            # Extract insights with configuration
            date_range = table_config.get('date_range')
            start_date = table_config.get('start_date')
            end_date = table_config.get('end_date')
            level = table_config.get('level', 'account')
            time_increment = table_config.get('time_increment', 'daily')
            
            return self.extract_insights(
                level=level,
                date_range=date_range,
                start_date=start_date,
                end_date=end_date,
                time_increment=time_increment,
                fields=fields if fields else None
            )
        else:
            raise ValueError(f"Unknown table name: {table_name}")
