library(ggplot2)
library(dplyr)
library(viridis)
library(colorspace)
library(RColorBrewer)
library(grid)
library(ggnewscale)
library(ggtext)
library(tidyverse)
library(shadowtext)
library(patchwork)
library(readxl)
library(reshape2)
library(scales)
library(rjson)
library(tibble)
library(stringr)
library(hrbrthemes)
library(lubridate)

# Data
comparisons <- read.csv('june_processed_data.csv')
comparisons <- subset(comparisons, select = -X)
comparisons <- na.omit(comparisons)
comparisons$sensor_index <- factor(comparisons$sensor_index)

mean_std_data <- comparisons %>%
  group_by(fields) %>%
  summarize(mean_val = mean(reading), std_dev = sd(reading))

mean_std_data <- mean_std_data %>%
  mutate(threshold = 2 * std_dev)

comparisons <- comparisons %>%
  inner_join(mean_std_data, by = "fields") %>%
  filter(abs(reading - mean_val) <= threshold)

comparisons <- comparisons %>%
  mutate(date_only = as.Date(datetime))

weekday_names <- c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
comparisons$day_of_week <- weekdays(as.Date(comparisons$day_of_week, origin = "1970-01-05"), abbreviate = FALSE)
comparisons$day_of_week <- factor(comparisons$day_of_week, levels = weekday_names)

bank_holidays <- c("2022-12-27", "2023-01-02", "2023-04-07", "2023-04-10", "2023-05-01", "2023-05-29")

comparisons$date_only <- as.Date(comparisons$date_only)
# Remove leading and trailing spaces from the 'date_only' column if needed
comparisons$date_only <- trimws(comparisons$date_only)

# Create the is_bank_holiday column
comparisons <- comparisons %>%
  mutate(is_bank_holiday = ifelse(date_only %in% bank_holidays, "Yes", "No"))

comparisons_no_bank_hols <- comparisons %>%
  filter(!(date_only %in% as.Date(bank_holidays)))

CAN_COLOURS <-  c("#3d5a80", "#98c1d9", "#ee6c4d", "#e0fbfc")

grouped_df <- aggregate(reading ~ sensor_index + fields, data = comparisons, FUN = mean)
plot1 <- ggplot(data = grouped_df, aes(x = sensor_index, y = reading, fill = fields)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(x = "Sensor", y = "Reading (μgm-3)", fill = "Pollutant") +
  scale_fill_manual(values = CAN_COLOURS) +
  ggtitle("Mean pollution levels") +
  theme_minimal() +
  theme(panel.grid = element_blank())

avg_data <- comparisons_no_bank_hols %>%
  group_by(day_of_week, fields) %>%
  summarize(avg_reading = mean(reading))
plot2 <- ggplot(avg_data, aes(x = day_of_week, y = avg_reading, group = fields, color = fields)) +
  geom_smooth(se = FALSE) +
  labs(x = "Day", y = "Mean reading (μgm-3)", color = "Pollutant") +
  ggtitle("How does pollution change across the week?") +
  scale_color_manual(values = CAN_COLOURS) +
  theme_minimal() +
  theme(panel.grid = element_blank())

avg_data <- comparisons %>%
  group_by(time, fields) %>%
  summarize(avg_reading = mean(reading))
avg_data$hour <- format(strptime(avg_data$time, "%H:%M:%S"), "%H")
plot3 <- ggplot(avg_data, aes(x = hour, y = avg_reading, group = fields, color = fields)) +
  geom_smooth(se = FALSE) +
  labs(x = "Hour of day", y = "Mean reading (μgm-3)", color = "Pollutant") +
  ggtitle("How does pollution change across the day?") +
  scale_color_manual(values = CAN_COLOURS) +
  theme_minimal() +
  theme(panel.grid = element_blank())

grouped_df <- aggregate(reading ~ fields + is_bank_holiday, data = comparisons, FUN = mean)
plot4 <- ggplot(grouped_df, aes(x = fields, y = reading, fill = is_bank_holiday)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(x = "Pollutant", y = "Mean reading (μgm-3)", fill = "Bank Holiday") +
  ggtitle("Do public holidays make a difference?") +
  scale_fill_manual(values = CAN_COLOURS) +
  theme_minimal() +
  theme(panel.grid = element_blank())

grouped_df <- aggregate(reading ~ date_only + fields, data = comparisons, FUN = mean)
grouped_df$date_only <- as.Date(grouped_df$date_only)
plot5 <- ggplot(grouped_df, aes(x = date_only, y = reading, group = fields, color = fields)) +
  geom_line() +
  labs(x = "Date", y = "Mean reading (μgm-3)", color = "Pollutant") +
  ggtitle("Mean daily reading") +
  scale_color_manual(values = CAN_COLOURS) +
  theme_minimal() +
  theme(panel.grid = element_blank()) +
  scale_x_date(labels = date_format("%Y-%m-%d"), breaks = "1 month")

pm_1 <- subset(comparisons, fields == "pm1.0_atm")
grouped_df <- aggregate(reading ~ date_only + fields, data = pm_1, FUN = mean)
grouped_df$date_only <- as.Date(grouped_df$date_only)
plot6 <- ggplot(grouped_df, aes(x = date_only, y = reading)) +
  geom_line() +
  labs(x = "Date", y = "Mean reading (μgm-3)") +
  ggtitle("PM1, mean daily reading") +
  geom_line(color = "#3d5a80")  +
  theme_minimal() +
  theme(panel.grid = element_blank()) +
  scale_x_date(labels = date_format("%Y-%m-%d"), breaks = "1 month")

pm_25 <- subset(comparisons, fields == "pm2.5_atm")
grouped_df <- aggregate(reading ~ date_only + fields, data = pm_25, FUN = mean)
grouped_df$date_only <- as.Date(grouped_df$date_only)
plot7 <- ggplot(grouped_df, aes(x = date_only, y = reading)) +
  geom_line() +
  labs(x = "Date", y = "Mean reading (μgm-3)") +
  ggtitle("PM2.5, mean daily reading") +
  geom_line(color = "#98c1d9")  +
  theme_minimal() +
  theme(panel.grid = element_blank()) +
  geom_hline(yintercept = 5, color = "#ee6c4d") +
  geom_hline(yintercept = 20, color = "#3d5a80") +
  scale_x_date(labels = date_format("%Y-%m-%d"), breaks = "1 month")

pm_10 <- subset(comparisons, fields == "pm10.0_atm")
grouped_df <- aggregate(reading ~ date_only + fields, data = pm_10, FUN = mean)
grouped_df$date_only <- as.Date(grouped_df$date_only)
plot8 <- ggplot(grouped_df, aes(x = date_only, y = reading)) +
  geom_line(color = "#98c1d9")  +
  labs(x = "Date", y = "Mean reading (μgm-3)") +
  ggtitle("PM10, mean daily reading") +
  theme_minimal() +
  theme(panel.grid = element_blank()) +
  geom_hline(yintercept = 15, color = "#ee6c4d") +
  geom_hline(yintercept = 40, color = "#3d5a80") +
  scale_x_date(labels = date_format("%Y-%m-%d"), breaks = "1 month")

subset_df <- subset(comparisons, fields = "pm1.0_atm")
plot9 <- ggplot(comparisons, aes(x = sensor_index, y = reading)) +
  geom_boxplot() +
  labs(x = "Sensor", y = "Reading (μgm-3)") +
  ggtitle("PM1 levels by sensor") +
  theme_minimal()

subset_df <- subset(comparisons, fields = "pm2.5_atm")
plot10 <- ggplot(comparisons, aes(x = sensor_index, y = reading)) +
  geom_boxplot() +
  labs(x = "Sensor", y = "Reading (μgm-3)") +
  ggtitle("PM2.5 levels by sensor") +
  theme_minimal()

subset_df <- subset(comparisons, fields = "pm10.0_atm")
plot11 <- ggplot(comparisons, aes(x = sensor_index, y = reading)) +
  geom_boxplot() +
  labs(x = "Sensor", y = "Reading (μgm-3)") +
  ggtitle("PM10 levels by sensor") +
  theme_minimal()