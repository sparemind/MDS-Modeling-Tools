# v1.5.1
# This program creates an MDS model of the given data and plots it and 
# goodness-of-fit statistics in several forms. The data should be given as a
# CSV file, with the first column containing the names of what each row is, and
# with the first row containing column headers.
#
# Several files will be generated:
# - plot.png        A wordcloud plot of the MDS model
# - plain_plot.png  An unlabeled plot of the MDS model
# - gof_dim.png     A plot of MDS goodness-of-fit vs. the MDS dimension
# - gof_exp.png     A plot of MDS goodness-of-fit vs. the Minkowski exponent
# - points.csv      A comma separated file of the xy-coordinates of the model
#                   along with their corresponding names. 
#
# All plots and data files will be saved in the current working directory.
#
# This program should be run as:
# $ Rscript MDS.R [colors]
# [colors] is an optional .csv file that specifies the r,g,b,a [0,1] values
# that each corresponding point should be colored with.
# 
# Notes on installing the necessary packages:
#   install.packages("wordcloud", repos="http://cran.us.r-project.org")
#   install.packages("RColorBrewer", repos="http://cran.us.r-project.org")
#   install.packages("scatterplot3d", repos="http://cran.us.r-project.org")
#
# Changelog v1.5.1
# - Added 3D color plotting
# - 1D plot now plots with the y-axis uniformly distributed
# Changelog v1.5
# - Added 1D plotting
# - Added 3D plotting
# Changelog v1.4
# - Added option to specify colors for each points for the unlabeled plot
# Changelog v1.3
# - Added unlabeled plot generation
# - Changed dimensions of word cloud plot to be more square
# - MDS points now saved to text file
# Changelog v1.2
# - Added plotting of goodness of fit vs. the MDS dimension
# - Added plotting of goodness of fit vs. the Minkowski exponent
# Changelog v1.1
# - Added ability to apply function to distances

# Check if file for colors was given
args = commandArgs(trailingOnly=TRUE)
colors_file = ""
if(length(args) != 0) {
    colors_file = args[1]
}

# Import data (and ignore first column, since it just has names)
raw_data <- read.csv(file="filtered.csv", head=TRUE, sep=",")
data = raw_data[-1]
names = t(raw_data[1])

# Function to apply to all distances
f <- function(x) {
    # return(abs(x)^0.5 * sign(x))
    return(x)
}

# Compute distances and MDS
distances = dist((apply(data, MARGIN=c(1,2), f)), method="minkowski", p=2)
mds <- cmdscale(distances, k=2)

# For the 1D plot
#uniform <- as.vector(rep(0, length(mds[,1])))
uniform <- runif(length(mds[,1]), -0.5, 0.5)

# For the 3D plot
#library("scatterplot3d")
#png(filename="3d_plain_plot.png")
#scatterplot3d(mds[,1], mds[,2], mds[,3], main="3D Plot")
#scatterplot3d(mds[,1], mds[,2], mds[,3], main="3D Plot", color=colors, pch=symbols)

# Create unlabeled plot. Color if a color file was given.
png(filename="plain_plot.png")
if(colors_file != "") {
    # Get point colors
    raw_colors <- read.csv(file=colors_file, head=FALSE, sep=",")
    colors <- vector("list", nrow(raw_colors))
    colors = c()
    symbols = c()
    for(i in 1:nrow(raw_colors)) {
        r = raw_colors[i,][1]
        g = raw_colors[i,][2]
        b = raw_colors[i,][3]
        a = raw_colors[i,][4]
        colors[i] = rgb(r, g, b, a)
        if(colors[i] == "#000000FF") {
            symbols[i] = 1
        } else {
            symbols[i] = 16
        }
    }
     
    plot(mds[,1], mds[,2], xlab="x", ylab="y", col=colors, pch=symbols)
    #plot(mds[,1], uniform, xlab="x", ylab="y", col=colors, pch=symbols, ylim=c(-3, 3))
} else {
    plot(mds[,1], mds[,2], xlab="x", ylab="y")
    #plot(mds[,1], uniform, xlab="x", ylab="y", ylim=c(-3, 3))
}

# Create wordcloud plot
library("wordcloud")
png(filename="plot.png", width=4000, height=4000, units="px")
textplot(mds[,1], mds[,2], names, cex=0.8)
#textplot(mds[,1], uniform, names, cex=0.8)

# Save MDS points to file
points <- paste(names, mds[,1], mds[,2], sep=",")
write(points, "points.csv")

# Plot goodness of fit vs. dimension
#DIM_MAX <- 10
#gofs_dim <- vector("list", DIM_MAX)
#for(i in 1:DIM_MAX) {
#    gofs_dim[[i]] <- cmdscale(distances, k=i, eig=TRUE)$GOF[1]
#}
#png(filename="gof_dim.png")
#plot(1:DIM_MAX, gofs_dim, xlab="MDS Dimension", ylab="MDS Goodness of Fit")

# Plot goodness of fit vs. Minkowski exponent
#EXP_MAX <- 10
#gofs_exp <- vector("list", EXP_MAX)
#for(i in 1:EXP_MAX) {
#    distances = dist((apply(data, MARGIN=c(1,2), f)), method="minkowski", p=i)
#    gofs_exp[[i]] <- cmdscale(distances, k=2, eig=TRUE)$GOF[1]
#}
#png(filename="gof_exp.png")
#plot(1:EXP_MAX, gofs_exp, xlab="Minkowski Exponent", ylab="MDS Goodness of Fit")

