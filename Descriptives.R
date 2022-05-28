###One participant's process data isn't being collected for whatever reason

process <- read.csv("~/Desktop/EDM Final Project/process.csv")
demos = read.csv("/Users/raypatt/Desktop/Motivation/Final\ Project/Fox\ and\ Field\ Participants\ Survey\ 1/demos.csv")
demos$Major = tolower(substr(demos$Major,1,2))

data = merge(process,demos)

novices = subset(data, Major == "ed" | Major == "ps")
experts = subset(data, Major == "en" | Major == "co")

data$noviceexpert = factor(data$Major)
levels(data$noviceexpert) = c("expert", "novice", "expert", "novice")

data_perparticipant = data[!duplicated(data$ID),]

##Action frequencies
tmp = data.frame(table(data$action))

##Cooccuring Actions
actions = data[3:11]
X <- as.matrix(actions)
out <- crossprod(X)  # Same as: t(X) %*% X
diag(out) <- 0       # (b/c you don't count co-occurrences of an aspect with itself)
out

###Major Table
table(data_perparticipant$Major)

###Gender Table
table(data_perparticipant$Gender)

###Ethnicity Table
table(data_perparticipant$Ethnicity2)

### Average Actions Per Level
data$Level_Broad = substr(data$levelID,1,1)
count_actions = aggregate(Email~ID+Level_Broad+noviceexpert,             # Input formula
                          data,                # List or data frame where the variables are stored
                          FUN = length)
count_actions_avg = aggregate(Email~Level_Broad+noviceexpert, count_actions, FUN = mean)
count_actions_sd = aggregate(Email~Level_Broad+noviceexpert, count_actions, FUN = sd)

### Average Levels per Participant
data$tmp = interaction(data$Email, data$Level_Broad)
data_perpartperlevel = data[!duplicated(data$tmp,),]

tmp = aggregate(ID~Level_Broad+noviceexpert,             # Input formula
                data_perpartperlevel,                # List or data frame where the variables are stored
                FUN = length)



data_perpartperlevel = data[!duplicated(data$tmp,),]

