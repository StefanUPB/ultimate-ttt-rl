__author__ = 'Shayak'
import vincent
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
import numpy as np

def setFontProperties():
    #fontProperties = {'family':'sans-serif','sans-serif':['Arial'], 'weight' : 'normal', 'size' : 12}
    #fontProperties = fm.FontProperties(fname='/Users/sevan/Library/Fonts/avenir-light.ttf')
    fontProperties = fm.FontProperties(fname='/Users/Shayak/Library/Fonts/avenir-light.ttf')
    matplotlib.rc('font', family=fontProperties.get_family())
    matplotlib.rc('font', serif=fontProperties.get_name())
    matplotlib.rc('text', usetex=False)
    matplotlib.rcParams.update({'font.size': 14})

def visualizeStateData(stateDict, dataBind, dataKey,
                       thresholds=None,
                       mapTitle=None,
                       jsonFile=None,
                       htmlFile=None):
    statePanda = {}
    stateCount = 0
    for (key, value) in stateDict.items():
        statePanda[stateCount] = [key, value]
        stateCount += 1
    stateData = pd.DataFrame.from_dict(statePanda, orient='index')
    stateData.columns = [dataKey, dataBind]
    visualizePandasData(stateData, dataBind, dataKey, thresholds, mapTitle, jsonFile, htmlFile)

def visualizePandasData(stateData,dataBind, dataKey,
                       thresholds=None,
                       mapTitle=None,
                       jsonFile=None,
                       htmlFile=None):
    state_topo = 'https://raw.githubusercontent.com/wrobstory/vincent_map_data/master/us_states.topo.json'
    geo_data = [{'name': 'states', 'url': state_topo, 'feature': 'us_states.geo'}]
    vis = vincent.Map(data=stateData, geo_data=geo_data, scale=1000,
                  projection='albersUsa', data_bind=dataBind, data_key=dataKey,
                  map_key={'states':'properties.NAME'}, brew='RdPu')
    vis.scales[0].type='threshold'
    vis.scales[0].domain = thresholds
    vis.legend(title=mapTitle)
    if jsonFile is not None and htmlFile is not None:
        vis.to_json(jsonFile, html_out=True, html_path=htmlFile)

def drawXYPlotByFactor(dataDict, xlabel='', ylabel='', legend=None,
                       title=None, logy=False, location=2):
    # Assuming that the data is in the format { factor: [(x1, y1),(x2,y2),...] }
    PLOT_STYLES = ['r^-', 'bo-', 'g^-', 'ks-', 'co-', 'ms-', 'y^-']
    styleCount = 0
    displayedPlots = []
    pltfn = plt.semilogy if logy else plt.plot
    for factor in dataDict:
        xpoints = [a[0] for a in dataDict[factor]]
        ypoints = [a[1] for a in dataDict[factor]]
        displayedPlots.append(pltfn(xpoints, ypoints, PLOT_STYLES[styleCount]))
        styleCount = min(styleCount+1, len(PLOT_STYLES)-1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if legend is None:
        plt.legend(dataDict.keys(), loc=location)
    else:
        plt.legend(legend, loc=location)
    if title is not None:
        plt.title(title)
    plt.show()

def drawGroupedBarChart(dataDict, xlabel='', ylabel='',
                        title=None, fileName=None):
    #PLOT_COLORS = ['r', 'b', 'g', 'y', 'c', 'm', 'k']
    PLOT_COLORS = ['0.25', '#009CE0', 'g', 'y', 'c', 'm', 'k']
    setFontProperties()
    index = np.arange(len(dataDict[dataDict.keys()[0]]))
    tickLabels = [u[0] for u in dataDict[dataDict.keys()[0]]]
    bar_width = 0.15
    opacity = 0.4
    rects = []
    for i, dataKey in enumerate(sorted(dataDict.keys())):
        color = PLOT_COLORS[min(len(PLOT_COLORS)-1, i)]
        data = [u[1] for u in sorted(dataDict[dataKey], key=lambda x: x[0])]
        rects.append(plt.bar(index+i*bar_width, data, bar_width,
                             alpha=opacity, color=color, linewidth=0, label=dataKey))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)
    plt.xticks(index + bar_width, tuple(tickLabels))
    plt.legend()
    if fileName is None:
        plt.show()
    else:
        plt.savefig(fileName)

def drawGroupedHistogram(dataDict, numBins=20, xlabel='', ylabel='', title=None, fileName=None):
    PLOT_COLORS = ['0.25', '#009CE0', 'g', 'y', 'c', 'm', 'k']
    #setFontProperties()
    for i, dataKey in enumerate(sorted(dataDict.keys())):
        color = PLOT_COLORS[min(len(PLOT_COLORS)-1, i)]
        plt.hist(dataDict[dataKey], bins=numBins, histtype='stepfilled',
                 color=color, alpha=0.4, linewidth=0, label=dataKey)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)
    plt.legend()
    if fileName is not None:
        plt.savefig(fileName)
    else:
        plt.show()