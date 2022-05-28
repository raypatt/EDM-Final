
library(tidyverse) #Data Manipulation and Plotting
library(lubridate) #Date Manipulation
library(arulesSequences) #Running the Sequence mining algorithm
library(ggtext) #Making adding some flair to plots
library(tidygraph)  ## Creating a Graph Structure
library(ggraph) ## Plotting the Network Graph Structure
library(dplyr)

process <- read.csv("~/Desktop/EDM Final Project/process.csv")
demos = read.csv("/Users/raypatt/Desktop/Motivation/Final\ Project/Fox\ and\ Field\ Participants\ Survey\ 1/demos.csv")
demos$Major = tolower(substr(demos$Major,1,2))

data = left_join(process, demos, by = "ID")

###experts and novices
novices = subset(data, Major == "ed" | Major == "ps")
experts = subset(data, Major == "en" | Major == "co")

novices = data.frame(sequenceID = as.integer(novices$seqId),
                     eventID = as.integer(novices$level),
                     item = as.factor(novices$action))
experts = data.frame(sequenceID = as.integer(experts$seqId),
                               eventID = as.integer(experts$level),
                               item = as.factor(experts$action))
#process$sequenceID = as.integer(process$seqId)
#process$eventID = as.integer(process$levelID)
#process$item = as.factor(process$action)
#process = process[c("sequenceID", "eventID", "item")]

novices = novices[
  with(novices, order(sequenceID, eventID)),
]
experts = experts[
  with(experts, order(sequenceID, eventID)),
]

experts_trans <-  as(experts %>% transmute(items = item), "transactions")
transactionInfo(experts_trans)$eventID <- as.integer(experts$eventID)
transactionInfo(experts_trans)$sequenceID = as.integer(experts$sequenceID)
itemLabels(experts_trans) <- str_replace_all(itemLabels(experts_trans), "items=", "")
expert_itemsets <- cspade(experts_trans, parameter = list(support = 0.4), control = list(verbose = FALSE))

novice_trans <-  as(novices %>% transmute(items = item), "transactions")
transactionInfo(novice_trans)$eventID <- as.integer(novices$eventID)
transactionInfo(novice_trans)$sequenceID = as.integer(novices$sequenceID)
itemLabels(novice_trans) <- str_replace_all(itemLabels(novice_trans), "items=", "")
novice_itemsets <- cspade(novice_trans, parameter = list(support = 0.4), control = list(verbose = FALSE))

#Convert Back to DS
expert_itemsets_df <- as(novice_itemsets, "data.frame") %>% as_tibble()

#Convert Back to DS
novice_itemsets_df <- as(expert_itemsets, "data.frame") %>% as_tibble()


write.csv(novice_itemsets_df,"novices.csv", row.names = FALSE)
write.csv(expert_itemsets_df,"experts.csv", row.names = FALSE)





exoert_rules <- ruleInduction(expert_itemsets, 
                       confidence = 0.6, 
                       control = list(verbose = FALSE))

exoert_rules_df <- as(exoert_rules, "data.frame") %>% 
  as_tibble() %>% 
  separate(col = rule, into = c('lhs', 'rhs'), sep = " => ", remove = F)




graph_dt <- experts %>% 
  group_by(sequenceID) %>% 
  transmute(eventID, source = item) %>% 
  mutate(destination = lead(source)) %>% 
  ungroup() %>%
  filter(!is.na(destination)) %>% 
  select(source, destination, sequenceID) %>% 
  count(source, destination, name = 'instances') 

g <- graph_dt %>% 
  filter(instances > 14) %>% 
  as_tbl_graph()
clp <- igraph::cluster_optimal(g)
g <- g %>% 
  activate("nodes") %>% 
  mutate(community = clp$membership)

set.seed(20201029)
ggraph(g, layout = 'fr') + 
  geom_node_voronoi(aes(fill = as.factor(community)), alpha = .4) + 
  geom_edge_parallel(aes(edge_alpha = log(instances)),
                     #color = "#5851DB",
                     edge_width = 1,
                     arrow = arrow(length = unit(4, 'mm')),
                     start_cap = circle(3, 'mm'),
                     end_cap = circle(3, 'mm')) +
  geom_node_point(fill = 'orange', size = 5, pch = 21) + 
  geom_node_text(aes(label = name), repel = T) + 
  labs(title = "My Browsing History",
       caption = "Minimum 15 Instances") + 
  scale_fill_viridis_d(guide = F) + 
  scale_edge_alpha_continuous(guide = F) + 
  theme_graph()



