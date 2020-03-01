'''
This is a sub-module of the portfolio-optimisation module for calculating different risk metrics
'''

import numpy as np
import pandas as pd


class RiskMetrics:
    '''
    This class contains methods for calculating common risk metrics used in trading and asset management.
    '''

    def __init__(self):
        return

    def calculate_variance(self, covariance, weights):
        '''
        Calculate variance of portfolio.

        :param covariance: (pd.DataFrame/np.matrix) covariance matrix of assets
        :param weights: (list) list of asset weights
        :return: (float) variance
        '''

        return np.dot(weights, np.dot(covariance, weights))

    def calculate_value_at_risk(self, returns, confidence_level=0.05):
        '''
        Calculate the value at risk (VaR) of the portfolio.

        :param returns: (pd.DataFrame/np.array) asset/portfolio historical returns
        :param confidence_level: (float) confidence level (alpha)
        :return: (float) VaR
        '''

        if not isinstance(returns, pd.DataFrame):
            returns = pd.DataFrame(returns)

        return returns.quantile(confidence_level, interpolation='higher')

    def calculate_expected_shortfall(self, returns, confidence_level=0.05):
        '''
        Calculate the expected shortfall (CVaR) of the portfolio.

        :param returns: (pd.DataFrame/np.array) asset/portfolio historical returns
        :param confidence_level: (float) confidence level (alpha)
        :return: (float) expected shortfall
        '''

        if not isinstance(returns, pd.DataFrame):
            returns = pd.DataFrame(returns)

        value_at_risk = self.calculate_value_at_risk(returns, confidence_level)
        expected_shortfall = np.nanmean(returns[returns < value_at_risk])
        return expected_shortfall

    def calculate_conditional_drawdown_risk(self, returns, confidence_level):
        '''
        Calculate the conditional drawdown of risk (CDaR) of the portfolio.

        :param returns: (pd.DataFrame/np.array) asset/portfolio historical returns
        :param confidence_level: (float) confidence level (alpha)
        :return: (float) conditional drawdown risk
        '''

        if not isinstance(returns, pd.DataFrame):
            returns = pd.DataFrame(returns)

        drawdown = returns.expanding().max() - returns
        max_drawdown = drawdown.expanding().max()
        max_drawdown_at_confidence_level = max_drawdown.quantile(confidence_level, interpolation='higher')
        conditional_drawdown = np.nanmean(max_drawdown[max_drawdown > max_drawdown_at_confidence_level])
        return conditional_drawdown