# Import Libraries

import os, datetime
import IPython, IPython.display
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf

mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['axes.grid'] = False

class Tensor:
    def __init__(self, x, y):
        self.x = pd.DataFrame(x, columns=['X'])
        self.y = pd.DataFrame(y, columns=['Y'])
    
    def Setup(self) -> pd.DataFrame:
        DataFrame = [self.x, self.y]

        df = pd.concat(DataFrame, axis= 1)

        n = len(df)
        Trainingdf = df[0:int(n*0.7)]
        Valuedf = df[int(n*0.7):int(n*0.9)]
        Testdf = df[int(n*0.9):]

        return df, Trainingdf, Valuedf, Testdf
    
    def NormalizeData(self):
        data, Training, Value, Testing = self.Setup()
        
        TrainingMean = Training.mean()
        TrainingStd = Training.std()

        Training = (Training - TrainingMean) / TrainingStd
        Value = (Value - TrainingMean) / TrainingStd
        Testing = (Testing - Training) / TrainingStd

        DataStd = (data - TrainingMean) / TrainingStd
        DataStd = DataStd.melt(var_name = 'Column', value_name='Normalized')

        return DataStd, Training, Value, Testing
    
#########################################################################
# Code From www.tensorflow.org
#########################################################################


class WindowGenerator():
    def __init__(self, InputWidth, LabelWidth, Shift, TrainDF: pd.DataFrame, ValueDF, TestDF, label_columns=None):
        # Storing the RAW Data
        self.TrainDf = TrainDF
        self.ValueDf = ValueDF
        self.TestDf = TestDF

        # Column Indicies
        self.LabelColumns = label_columns

        if label_columns is not None:
            self.LabelColumnsIndicies = {name: i for i, name in enumerate(label_columns)}
        
        self.ColumnIndices = {name: i for i, name in enumerate(TrainDF.columns)}

        # Window Params
        self.InputWidth = InputWidth
        self.LabelWidth = LabelWidth

        self.TotalWinSize = InputWidth + Shift

        self.InputSlice = slice(0, InputWidth)
        self.InputIndices = np.arange(self.TotalWinSize)[self.InputSlice]

        self.LabelStart = self.TotalWinSize - self.LabelWidth
        self.LabelSlice = slice(self.LabelStart, None)
        self.LabelIndices = np.arange(self.TotalWinSize)[self.LabelSlice]

    def __repr__(self):
        return 'n'.join([
            f'Total Window Size: {self.TotalWinSize}'
            f'Input Indices: {self.InputIndices}'
            f'Label Indices: {self.LabelIndices}'
            f'Label Column Name(s): {self.LabelColumns}'
        ])

    def SplitWindow(self, Features):
        Inputs = Features[:, self.InputSlice, :]    
        Labels = Features[:, self.LabelSlice, :]

        if self.LabelColumns is not None:
            Labels = tf.stack(
                [Labels[:, :, self.ColumnIndices[name]] for name in self.LabelColumns],
                axis = -1
            )
        
        Inputs.set_shape([None, self.InputWidth, None])
        Labels.set_shape([None, self.LabelWidth, None])

        return Inputs, Labels
    
    def Plot(self, Inputs, Labels, model=None, plot_col = 'X', max_subplots = 3):
        inputs, labels = Inputs, Labels 
        plt.figure(figsize=(12, 8))

        PlotColIndex = self.ColumnIndices[plot_col]
        MaxN = min(max_subplots, len(inputs))

        for n in range(MaxN):
            plt.subplot(MaxN, 1, n+1)
            plt.ylabel(f'{plot_col} [normed]')
            plt.plot(self.InputIndices, inputs[n, :, PlotColIndex], label = 'Input', marker='.', zorder= -10)
        
        if self.LabelColumns:
            LabelColIndex = self.LabelColumnsIndicies.get(plot_col, None)

        else:
            LabelColIndex = PlotColIndex

        plt.scatter(self.LabelIndices, labels[n, :, LabelColIndex], edgecolors='k', label = 'Labels', c='#2CA02C', s=64)

        if model is not None:
            predictions = model(inputs)
            plt.scatter(self.LabelIndices, predictions[n, :, LabelColIndex], marker='X', edgecolors='k', label='Predictions', c='#FF7F0E', s=64)
        
        if n == 0:
            plt.legend()
        
        plt.xlabel('Time')
