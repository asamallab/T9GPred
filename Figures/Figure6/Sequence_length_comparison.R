#library
library(dplyr)
library(ggplot2)
library(readr)
#library(ggsignif)
#library(dplyr)
library(ggpubr)
library(rstatix)
#reading the dataset
Bacteroidetes_402_sequence_length_CTD_statistics <- read_delim("Bacteroidetes_402_sequence_length_CTD_statistics.txt", 
                                                               delim = "\t", escape_double = FALSE, 
                                                               trim_ws = TRUE)

#Creation of a dataset for boxplot

data_boxplot <- Bacteroidetes_402_sequence_length_CTD_statistics[c('Sequence-length','motility')]

#Renaming columns and values

data_boxplot <- plyr::rename(data_boxplot,c('motility'='Gliding_motility'))
data_boxplot <- plyr::rename(data_boxplot,c('Sequence-length'='Sequence_length'))
data_boxplot$Gliding_motility[data_boxplot$Gliding_motility == 1] <- 'Present'
data_boxplot$Gliding_motility[data_boxplot$Gliding_motility == 0] <- 'Absent'
data_boxplot$Gliding_motility <- factor(data_boxplot$Gliding_motility, levels = c("Absent","Present"))

#---------------------------------------------------------


#statistical test (independent t-test)
stat.test <- data_boxplot %>%
  t_test(Sequence_length ~ Gliding_motility) %>%
  adjust_pvalue(method = "bonferroni") %>%
  add_significance("p.adj")
stat.test


# Create a box plot
bxp <- ggboxplot(
  data_boxplot, x = "Gliding_motility", y = "Sequence_length", 
  color = "Gliding_motility", palette = c("#F16767","#7DB9B6")
)

# Add p-values onto the box plots
stat.test <- stat.test %>%
  add_xy_position(x = "Gliding_motility", dodge = 0.8)
bxp + stat_pvalue_manual(
  stat.test,  label = "p", tip.length = 0
)

# Add 10% spaces between the p-value labels and the plot border
bxp + stat_pvalue_manual(
  stat.test,  label = "p", tip.length = 0
) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.1)))

# Use adjusted p-values as labels
# Remove brackets
bxp + stat_pvalue_manual(
  stat.test,  label = "p.adj", tip.length = 0,
  remove.bracket = TRUE
)

# Show adjusted p-values and significance levels
# Hide ns (non-significant)
bxp + stat_pvalue_manual(
  stat.test,  label = "{p.adj.signif}",#"{p.adj}{p.adj.signif}", 
  tip.length = 0, hide.ns = TRUE
) + labs(color='Gliding motility',x='Gliding motility',y='Genome size (kb)')

