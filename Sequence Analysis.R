behaviors <- read.csv("~/Desktop/EDM Final Project/behaviors.csv")

expert_string = levels(factor(behaviors$Class))[1]
novice_string = levels(factor(behaviors$Class))[2]

novices = subset(behaviors, Class == novice_string)
expert = subset(behaviors, Class == expert_string)

novices[order(-novices$Rate), ]
head(expert[order(-expert$Rate), ])
