"""
Facebook Ads Extractor
Extracts data from Facebook Ads API
"""
import logging
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
            
            FacebookAdsApi.init(app_id, app_secret, access_token)
            self.api = FacebookAdsApi.get_default_api()
            
            ad_account_id = self.config.get('ad_account_id')
            self.ad_account = AdAccount(ad_account_id)
            
            logger.info(f"Facebook Ads API initialized for account: {ad_account_id}")
            
        except Exception as e:
            logger.error(f"Error initializing Facebook Ads API: {e}")
            raise
    
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
                Ad.Field.creative,
                Ad.Field.created_time,
                Ad.Field.updated_time,
            ]
        
        try:
            logger.info("Extracting ads from Facebook Ads...")
            ads = self.ad_account.get_ads(fields=fields)
            
            data = []
            for ad in ads:
                ad_dict = dict(ad)
                # Flatten creative object if present
                if 'creative' in ad_dict and isinstance(ad_dict['creative'], dict):
                    ad_dict['creative_id'] = ad_dict['creative'].get('id')
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
        date_range: int = 30,
        fields: List[str] = None
    ) -> pd.DataFrame:
        """
        Extract insights (metrics) from Facebook Ads
        
        Args:
            level: Aggregation level ('account', 'campaign', 'adset', 'ad')
            date_range: Number of days to look back
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
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=date_range)
        
        params = {
            'level': level,
            'time_range': {
                'since': start_date.strftime('%Y-%m-%d'),
                'until': end_date.strftime('%Y-%m-%d')
            },
            'time_increment': 1,  # Daily breakdown
        }
        
        try:
            logger.info(f"Extracting insights from Facebook Ads (level={level}, date_range={date_range} days)...")
            insights = self.ad_account.get_insights(fields=fields, params=params)
            
            data = []
            for insight in insights:
                data.append(dict(insight))
            
            df = pd.DataFrame(data)
            
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
            date_range = table_config.get('date_range', 30)
            level = table_config.get('level', 'account')
            return self.extract_insights(
                level=level,
                date_range=date_range,
                fields=fields if fields else None
            )
        else:
            raise ValueError(f"Unknown table name: {table_name}")
