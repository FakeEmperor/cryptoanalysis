"""
Utils for crypto analysis
"""
import numpy as np

from .frequency import GramStat


def log_loss(predicted: GramStat, actual: GramStat) -> float:
    """
    Logarithmic loss over frequency of predicted ngram and actual ngram
    """
    loss = 0
    for pred_label in predicted.keys():
        loss -= np.log(actual.get(pred_label, actual.min_frequency[1]))
    return loss


def abs_loss(predicted: GramStat, actual: GramStat) -> float:
    loss = 0
    for pred_label, pred_freq in predicted.items():
        loss += np.abs(pred_freq - actual.get(pred_label, actual.min_frequency[1]))
    return loss
