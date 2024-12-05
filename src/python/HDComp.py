# # Code Objective
# # The purpose of this program is to implement a Resonator Network algorithm that solves factorization problems for high-dimensional vectors.
# # It uses Hyperdimensional Computing (HDC) principles to encode, bind, and disentangle information about three features: color, shape, and position.
# # The network converges through iterations to identify the most similar vector (from a predefined codebook) for each feature.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

# This function identifies the vector in a codebook that is most similar to the input vector vec.
# Similarity is measured based on the number of matching elements (using a dot product).
def greatestSim(vec, codebook): #function for similarity search. Returns vector in codebook most similar to input vec
    bestmatch = 0
    bestCode = codebook[0]
    for code in codebook:
        codeCorrect = vec * code
        numCorrect = np.count_nonzero(codeCorrect == 1)
        if(numCorrect > bestmatch):
            bestmatch = numCorrect
            bestCode = code

    return bestCode

def resonatorNet(color, shape, position, s, XXt, YYt, ZZt, Xt, Yt, Zt, red, blue, green, circle, square, triangle, topleft, topright, bottomleft, bottomright, maxIter=100):
    xHat = red + blue + green #initial xhat value (superimposed vectors)
    xHat[xHat>=0] = 1
    xHat[xHat<0] = -1
    yHat = circle + square + triangle #initial yhat value (superimposed vectors)
    yHat[yHat>=0] = 1
    yHat[yHat<0] = -1
    zHat = topleft + topright + bottomleft + bottomright #initial zhat value (superimposed vectors)
    zHat[zHat>=0] = 1
    zHat[zHat<0] = -1
    settled = [0] * 3

    similarity_history = {'color': [], 'shape': [], 'position': []}

    for i in range(maxIter): #iterate until convergence is reached or maximum iterations reached
        xHatn = s * yHat * zHat #binding operations
        yHatn = s * xHat * zHat
        zHatn = s * xHat * yHat
        #if(settled[0] == 0): #if xHat has settled do not calculate new value
        xHat = np.matmul(XXt, xHatn)
        xHat[xHat>=0] = 1
        xHat[xHat<0] = -1
        #if(settled[1] == 0): #if yHat has settled do not calculate new value
        yHat = np.matmul(YYt, yHatn)
        yHat[yHat>=0] = 1
        yHat[yHat<0] = -1
        #if(settled[2] == 0): #if zHat has settled do not calculate new value
        zHat = np.matmul(ZZt, zHatn)
        zHat[zHat>=0] = 1
        zHat[zHat<0] = -1

        # Track similarities
        # Track similarities
        similarity_history['color'].append({
            'red': np.mean(red == xHat),
            'blue': np.mean(blue == xHat),
            'green': np.mean(green == xHat),
        })
        similarity_history['shape'].append({
            'circle': np.mean(circle == yHat),
            'square': np.mean(square == yHat),
            'triangle': np.mean(triangle == yHat),
        })
        similarity_history['position'].append({
            'topleft': np.mean(topleft == zHat),
            'topright': np.mean(topright == zHat),
            'bottomleft': np.mean(bottomleft == zHat),
            'bottomright': np.mean(bottomright == zHat),
        })

        settled = [0] * 3
        if np.array_equal(xHat, xHatn): #check for convergence of xHat
            settled[0] = 1
        if np.array_equal(yHat, yHatn): #check for convergence of yHat
            settled[1] = 1
        if np.array_equal(zHat, zHatn): #check for convergence of zHat
            settled[2] = 1
        if(settled.count(1) == 3): #if all have converged then stop iterating
            break

    # simX = greatestSim(xHat, Xt) #find vector in codebook most similar to converged xHat
    # simY = greatestSim(yHat, Yt) #find vector in codebook most similar to converged yHat
    # simZ = greatestSim(zHat, Zt) #find vector in codebook most similar to converged zHat
    # xCorrect = color * simX #see similarity between the correct color and xHat
    # yCorrect = shape * simY #see similarity between the correct color and yHat
    # zCorrect = position * simZ #see similarity between the correct color and zHat
    # if debug: #print stats if debug is enabled
    #     print(f'S = {s}')
    #     print(f'Orginal Color Vector: {color} Disentangled {xHat}, correct bits {np.count_nonzero(xCorrect == 1)}') #see how correct xHat is
    #     print(f'Orginal Color Vector: {shape} Disentangled {yHat}, correct bits {np.count_nonzero(yCorrect == 1)}') #see how correct yHat is
    #     print(f'Orginal Color Vector: {position} Disentangled {zHat}, correct bits {np.count_nonzero(zCorrect == 1)}') #see how correct xHat is
    #     print(f'Iterations: {i+1}') #print number of resonator network iterations
    #     if(settled.count(1) == 3): #print whether network converged
    #         print('Convergence Reached')
    return similarity_history
    # if(np.array_equal(simX, color) and np.array_equal(simY, shape) and np.array_equal(simZ, position)): #check whether results are correct
    #     return 1
    # return 0

###################################################################################################

# Set FiveThirtyEight style globally
plt.style.use('fivethirtyeight')


######################### Choose the case of Red, Center, Circle ###################################

# Function to run a single case
def run_single_case(vecSize, maxIter, chosen_color, chosen_shape, chosen_position):
    #Xt = np.random.randint(2, size=(3, vecSize))
    #Yt = np.random.randint(2, size=(3, vecSize))
    #Zt = np.random.randint(2, size=(3, vecSize))
    #Xt[Xt == 0] = -1
    #Yt[Yt == 0] = -1
    #Zt[Zt == 0] = -1
    with open('codebooks.npy', 'rb') as codefd:
        Xt = np.load(codefd)
        Yt = np.load(codefd)
        Zt = np.load(codefd)
    X, Y, Z = Xt.T, Yt.T, Zt.T
    XXt, YYt, ZZt = np.sign(np.matmul(X, Xt)), np.sign(np.matmul(Y, Yt)), np.sign(np.matmul(Z, Zt))
    red = np.transpose(Xt[0]) #color vectors
    blue = np.transpose(Xt[1])
    green = np.transpose(Xt[2])
    circle = np.transpose(Yt[0]) #shape vectors
    square = np.transpose(Yt[1])
    triangle = np.transpose(Yt[2])
    topleft = np.transpose(Zt[0]) #position vectors
    topright = np.transpose(Zt[1])
    bottomleft = np.transpose(Zt[2])
    bottomright = np.transpose(Zt[3])

    color_map = {'red': red, 'blue': blue, 'green': green}
    shape_map = {'circle': circle, 'square': square, 'triangle': triangle}
    position_map = {'topleft': topleft, 'topright': topright, 'bottomleft': bottomleft, 'bottomright': bottomright}

    color = color_map[chosen_color]
    shape = shape_map[chosen_shape]
    position = position_map[chosen_position]

    s = color * shape * position
    history = resonatorNet(color, shape, position, s, XXt, YYt, ZZt, Xt, Yt, Zt, red, blue, green,
                           circle, square, triangle, topleft, topright, bottomleft, bottomright, maxIter)
    return history

# Plotting function for shape, color, and position graphs
# def plot_graph(similarity_history, category, title, colors):
#     plt.figure(figsize=(6, 4))
#     fig, ax = plt.subplots()
#     ax.set_facecolor('#E6E6E6')  # Set gray background
#     ax.set_axisbelow(True)       # Make gridlines appear below the plot lines
#     ax.grid(color='white', linestyle='--', linewidth=0.7, alpha=0.7)  # Light white grid

#     for key, color in colors.items():
#         values = [entry[key] for entry in similarity_history[category]]
#         ax.plot(range(len(values)), values, label=f"{key.capitalize()} Similarity", color=color, linewidth=3.0)

#     ax.set_title(title, fontsize=18, fontweight='bold')
#     ax.set_xlabel("Iterations", fontsize=14, fontweight='bold')
#     ax.set_ylabel("Similarity", fontsize=14, fontweight='bold')
#     ax.legend(fontsize=12)
#     plt.tight_layout()
#     plt.show()

def plot_graph(similarity_history, category, title, colors, position='single'):
    # Create the figure and axes with different layouts
    if position == 'single':
        plt.figure(figsize=(6, 4))
        fig, ax = plt.subplots()
        ax.set_facecolor('#E6E6E6')  # Set gray background
        ax.set_axisbelow(True)       # Make gridlines appear below the plot lines
        ax.grid(color='white', linestyle='--', linewidth=0.7, alpha=0.7)  # Light white grid
        
        for key, color in colors.items():
            values = [entry[key] for entry in similarity_history[category]]
            ax.plot(range(len(values)), values, label=f"{key.capitalize()} Similarity", color=color, linewidth=3.0)
        
        ax.set_title(title, fontsize=18, fontweight='bold')
        ax.set_xlabel("Iterations", fontsize=14, fontweight='bold')
        ax.set_ylabel("Similarity", fontsize=14, fontweight='bold')
        ax.legend(fontsize=12)
        plt.tight_layout()
        plt.show()

    elif position == 'multi':
        # Create a 2x2 layout (2 rows, 2 columns) for multiple graphs
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        # First plot on the top-left
        axes[0, 0].set_facecolor('#E6E6E6')
        axes[0, 0].set_axisbelow(True)
        axes[0, 0].grid(color='white', linestyle='--', linewidth=0.7, alpha=0.7)
        for key, color in colors.items():
            values = [entry[key] for entry in similarity_history[category]]
            axes[0, 0].plot(range(len(values)), values, label=f"{key.capitalize()} Similarity", color=color, linewidth=3.0)
        axes[0, 0].set_title('Shape Similarity Evolution', fontsize=18, fontweight='bold')
        axes[0, 0].set_xlabel("Iterations", fontsize=14, fontweight='bold')
        axes[0, 0].set_ylabel("Similarity", fontsize=14, fontweight='bold')

        # Second plot on the top-right
        axes[0, 1].set_facecolor('#E6E6E6')
        axes[0, 1].set_axisbelow(True)
        axes[0, 1].grid(color='white', linestyle='--', linewidth=0.7, alpha=0.7)
        for key, color in colors.items():
            values = [entry[key] for entry in similarity_history[category]]
            axes[0, 1].plot(range(len(values)), values, label=f"{key.capitalize()} Similarity", color=color, linewidth=3.0)
        axes[0, 1].set_title('Color Similarity Evolution', fontsize=18, fontweight='bold')
        axes[0, 1].set_xlabel("Iterations", fontsize=14, fontweight='bold')
        axes[0, 1].set_ylabel("Similarity", fontsize=14, fontweight='bold')

        # Third plot on the bottom-left (centered on bottom row)
        axes[1, 0].set_facecolor('#E6E6E6')
        axes[1, 0].set_axisbelow(True)
        axes[1, 0].grid(color='white', linestyle='--', linewidth=0.7, alpha=0.7)
        for key, color in colors.items():
            values = [entry[key] for entry in similarity_history[category]]
            axes[1, 0].plot(range(len(values)), values, label=f"{key.capitalize()} Similarity", color=color, linewidth=3.0)
        axes[1, 0].set_title('Position Similarity Evolution', fontsize=18, fontweight='bold')
        axes[1, 0].set_xlabel("Iterations", fontsize=14, fontweight='bold')
        axes[1, 0].set_ylabel("Similarity", fontsize=14, fontweight='bold')

        # Remove the empty space in the bottom-right corner
        fig.delaxes(axes[1, 1])

        # Adjust layout for better spacing
        plt.tight_layout()
        plt.show()

# Example: Generate similarity histories and plots
if __name__ == '__main__':
    vecSize = 32
    maxIter = 100
    chosen_color = 'red'
    chosen_shape = 'circle'
    chosen_position = 'bottomright'

    history = run_single_case(vecSize, maxIter, chosen_color, chosen_shape, chosen_position)

    # Plot Shape Similarities
    plot_graph(history, category='shape', title="Shape Similarity Evolution (Triangle, Circle, Square)",
            colors={'triangle': 'blue', 'circle': 'green', 'square': 'red'})

    # Plot Color Similarities
    plot_graph(history, category='color', title="Color Similarity Evolution (Red, Blue, Green)",
            colors={'red': 'red', 'blue': 'blue', 'green': 'green'})

    # Plot Position Similarities
    plot_graph(history, category='position', title="Position Similarity Evolution (Top Left, Top Right, Bottom Left, Bottom Right)",
            colors={'topleft': 'blue', 'topright': 'green', 'bottomleft': 'red', 'bottomright': 'magenta'})
