library(tidyverse)
forms <- read.csv("cldf/forms.csv")
str(forms$Value)

forms %>%
  dplyr::select( -Form) %>%
  mutate(Form = Value) %>%
  separate_longer_delim(Form, delim = "; ")%>%
  separate_longer_delim(Form, delim = ", ") %>%
  relocate(Form, .after = Value) -> forms_split


write.csv(forms_split,"etc/forms_split.csv")

  
  
  
  
