import numpy as np
import pandas as pd
from rich.console import Console
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

console = Console()

class TradingSignalEngine:
    """Engine untuk menghasilkan sinyal trading yang akurat"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        
    def prepare_features(self, df):
        """Menyiapkan fitur untuk machine learning"""
        features = []
        
        # Price-based features
        features.extend([
            'RSI', 'MACD', 'MACD_Signal', 'MACD_Histogram',
            '%K', '%D', 'Williams_R', 'CCI', 'ADX',
            'BB_Width', 'ATR_Percent', 'Trend_Strength'
        ])
        
        # Moving average ratios
        if f'EMA_12' in df.columns and f'EMA_26' in df.columns:
            df['EMA_Ratio'] = df['EMA_12'] / df['EMA_26']
            features.append('EMA_Ratio')
        
        # Price position in Bollinger Bands
        if all(col in df.columns for col in ['close', 'BB_Upper', 'BB_Lower']):
            df['BB_Position'] = (df['close'] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])
            features.append('BB_Position')
        
        # Volume analysis
        if 'volume' in df.columns:
            df['Volume_SMA'] = df['volume'].rolling(20).mean()
            df['Volume_Ratio'] = df['volume'] / df['Volume_SMA']
            features.append('Volume_Ratio')
        
        return df[features].fillna(0)
    
    def generate_labels(self, df, lookahead=5, threshold=0.02):
        """Generate labels untuk training (1=buy, 0=hold, -1=sell)"""
        future_returns = df['close'].shift(-lookahead) / df['close'] - 1
        
        labels = np.where(future_returns > threshold, 1,
                         np.where(future_returns < -threshold, -1, 0))
        
        return labels[:-lookahead]  # Remove last few rows
    
    def train_model(self, df):
        """Train machine learning model"""
        console.log("[cyan]🤖 Training ML model...[/cyan]")
        
        features = self.prepare_features(df)
        labels = self.generate_labels(df)
        
        # Ensure same length
        min_len = min(len(features), len(labels))
        features = features.iloc[:min_len]
        labels = labels[:min_len]
        
        # Remove rows with all zeros
        valid_rows = ~(features == 0).all(axis=1)
        features = features[valid_rows]
        labels = labels[valid_rows]
        
        if len(features) > 50:  # Minimum data requirement
            # Scale features
            features_scaled = self.scaler.fit_transform(features)
            
            # Train model
            self.model.fit(features_scaled, labels)
            self.is_trained = True
            
            console.log("[green]✅ Model berhasil ditraining![/green]")
        else:
            console.log("[yellow]⚠️ Data tidak cukup untuk training model[/yellow]")
    
    def predict_signals(self, df):
        """Prediksi sinyal menggunakan trained model"""
        if not self.is_trained:
            self.train_model(df)
        
        if self.is_trained:
            features = self.prepare_features(df)
            features_scaled = self.scaler.transform(features)
            
            predictions = self.model.predict(features_scaled)
            probabilities = self.model.predict_proba(features_scaled)
            
            df['ML_Signal'] = predictions
            df['ML_Confidence'] = np.max(probabilities, axis=1) * 100
            
        return df
    
    def calculate_risk_metrics(self, df, current_price):
        """Menghitung metrik risiko untuk position sizing"""
        console.log("[cyan]📊 Menghitung risk metrics...[/cyan]")
        
        # ATR-based stop loss
        atr = df['ATR'].iloc[-1] if 'ATR' in df.columns else current_price * 0.02
        
        # Support/Resistance levels
        support = df['Support_1'].iloc[-1] if 'Support_1' in df.columns else current_price * 0.98
        resistance = df['Resistance_1'].iloc[-1] if 'Resistance_1' in df.columns else current_price * 1.02
        
        # Volatility
        volatility = df['close'].pct_change().std() * np.sqrt(24) * 100  # Daily volatility %
        
        return {
            'atr': atr,
            'support': support,
            'resistance': resistance,
            'volatility': volatility,
            'atr_percent': (atr / current_price) * 100
        }
    
    def generate_trading_recommendation(self, df, symbol, timeframe):
        """Generate comprehensive trading recommendation"""
        console.log("[cyan]🎯 Generating trading recommendation...[/cyan]")
        
        if df.empty:
            return {"error": "No data available"}
        
        # Get latest data
        latest = df.iloc[-1]
        current_price = latest['close']
        
        # Predict signals
        df = self.predict_signals(df)
        
        # Calculate risk metrics
        risk_metrics = self.calculate_risk_metrics(df, current_price)
        
        # Combine signals
        technical_score = latest.get('Signal_Score', 0)
        ml_signal = latest.get('ML_Signal', 0)
        ml_confidence = latest.get('ML_Confidence', 0)
        
        # Final recommendation logic
        combined_score = (technical_score * 0.6) + (ml_signal * 0.4)
        
        if combined_score >= 2:
            action = "STRONG_BUY"
            confidence = min(90, 60 + ml_confidence * 0.3)
        elif combined_score >= 1:
            action = "BUY"
            confidence = min(80, 50 + ml_confidence * 0.3)
        elif combined_score <= -2:
            action = "STRONG_SELL"
            confidence = min(90, 60 + ml_confidence * 0.3)
        elif combined_score <= -1:
            action = "SELL"
            confidence = min(80, 50 + ml_confidence * 0.3)
        else:
            action = "HOLD"
            confidence = 50
        
        # Calculate entry, stop loss, and take profit
        atr_multiplier = 2.0 if timeframe in ['1m', '5m'] else 1.5
        
        if action in ["BUY", "STRONG_BUY"]:
            entry_price = current_price
            stop_loss = current_price - (risk_metrics['atr'] * atr_multiplier)
            take_profit_1 = current_price + (risk_metrics['atr'] * atr_multiplier * 1.5)
            take_profit_2 = current_price + (risk_metrics['atr'] * atr_multiplier * 2.5)
        elif action in ["SELL", "STRONG_SELL"]:
            entry_price = current_price
            stop_loss = current_price + (risk_metrics['atr'] * atr_multiplier)
            take_profit_1 = current_price - (risk_metrics['atr'] * atr_multiplier * 1.5)
            take_profit_2 = current_price - (risk_metrics['atr'] * atr_multiplier * 2.5)
        else:
            entry_price = current_price
            stop_loss = current_price
            take_profit_1 = current_price
            take_profit_2 = current_price
        
        # Risk/Reward ratio
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit_1 - entry_price)
        rr_ratio = reward / risk if risk > 0 else 0
        
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "action": action,
            "confidence": round(confidence, 1),
            "entry_price": round(entry_price, 6),
            "stop_loss": round(stop_loss, 6),
            "take_profit_1": round(take_profit_1, 6),
            "take_profit_2": round(take_profit_2, 6),
            "risk_reward_ratio": round(rr_ratio, 2),
            "technical_score": technical_score,
            "ml_signal": ml_signal,
            "ml_confidence": round(ml_confidence, 1),
            "volatility": round(risk_metrics['volatility'], 2),
            "atr_percent": round(risk_metrics['atr_percent'], 2),
            "support": round(risk_metrics['support'], 6),
            "resistance": round(risk_metrics['resistance'], 6),
            "current_rsi": round(latest.get('RSI', 50), 2),
            "current_macd": round(latest.get('MACD', 0), 6),
            "trend_strength": round(latest.get('Trend_Strength', 0), 4)
        }

# Global instance
signal_engine = TradingSignalEngine()
