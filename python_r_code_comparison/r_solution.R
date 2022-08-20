
library(dplyr)
library(tidyr)

# Initial solution (12 steps)
res <- read.csv('data.csv') %>% 
  mutate(Date = paste(Month, Year)) %>%
  mutate(Variable = factor(Variable, levels = c('Salary', 'Taxes', 'Bonus'))) %>% 
  select(-Month, -Year, -Name) %>% 
  complete(Date = paste(month.abb, 2022), nesting(Variable)) %>% 
  mutate(Date = factor(Date, levels = paste(month.abb, 2022))) %>%
  arrange(Date, Variable) %>% 
  replace_na(list(Amount = 0)) %>% 
  pivot_wider(names_from = Date, values_from = Amount) %>% 
  bind_rows(summarise(., across(where(is.numeric), sum, na.rm = T), across(where(is.factor), ~"TotalBrutto"))) %>% 
  rowwise() %>% 
  mutate(`Year Total` = sum(across(-Variable)))

#Second iteration (9 steps)
res <- read.csv('data.csv') %>% 
  mutate(Date = paste(Month, Year)) %>%
  select(-Month, -Year, -Name) %>% 
  mutate(Variable = factor(Variable, levels = c('Salary', 'Taxes', 'Bonus'))) %>% 
  mutate(Date = factor(Date, levels = paste(month.abb, 2022))) %>%
  complete(Date, nesting(Variable), fill = list(Amount = 0)) %>% 
  pivot_wider(names_from = Date, values_from = Amount) %>% 
  bind_rows(summarise(., across(where(is.numeric), sum, na.rm = T), across(Variable, ~"TotalNetto"))) %>% 
  rowwise() %>% 
  mutate(`Year Total` = sum(across(-Variable)))

# Third iteration (with janitor), 7 steps!
res <- read.csv('data.csv') %>% 
  mutate(Date = paste(Month, Year)) %>%
  select(-Month, -Year, -Name) %>% 
  mutate(Variable = factor(Variable, levels = c('Salary', 'Taxes', 'Bonus'))) %>% 
  mutate(Date = factor(Date, levels = paste(month.abb, 2022))) %>%
  complete(Date, nesting(Variable), fill = list(Amount = 0)) %>% 
  pivot_wider(names_from = Date, values_from = Amount) %>% 
  janitor::adorn_totals(c("row","col"), name = c('TotalNetto', 'Year Total'))

