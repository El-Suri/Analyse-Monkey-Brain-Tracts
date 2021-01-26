library(tidyverse)
library(ggpubr)
library(rstatix)

# Eickhoff = '/cubric/data/c1639425/Monkey_Brains/results_df/proportion_eickhoff_streamline_corrected_bst_subic_ncc_ant_thal_extglobpal_df'
# geschwind = /cubric/data/c1639425/Monkey_Brains/results_df/proportion_gschwind_bst_ncc_subic_antthal_globpal_df
# Eichoff cols = Subjects,subic_bst,subic_ant_thal,subic_ncc,subic_ext_glob_pal
#geschwind cols = Subjects,bst_subic,subic_ant_thal,ncc_subic,subic_ext_glob_pal
df_wide = read_csv('/cubric/data/c1639425/Monkey_Brains/results_df/proportion_gschwind_bst_ncc_subic_antthal_globpal_df')

df_wide = df_wide %>%
  select(Subjects,bst_subic,subic_ant_thal,ncc_subic,subic_ext_glob_pal)

print(df_wide)

df <- df_wide %>%
  gather(key = "ROI", value = "proportion",bst_subic,subic_ant_thal,ncc_subic,subic_ext_glob_pal) %>%
  convert_as_factor(Subjects, ROI)
print(df)

sumstats <- df %>%
  group_by(ROI) %>%
  get_summary_stats(proportion, type = "mean_sd")
print(sumstats)

bxp <- ggboxplot(df, x = "ROI", y = "proportion", add = "point")
bxp

# Test for outliers
outliers <- df %>%
  group_by(ROI) %>%
  identify_outliers(proportion)
print(outliers)

# Replace outliers, easier to do this in the wide Df

# Remove completely 
# df_outliers_rm <- df_wide %>% filter(subic_ext_glob_pal < 0.0204)


df_outliers_rm <- df_wide %>% mutate(subic_ext_glob_pal=replace(subic_ext_glob_pal, subic_ext_glob_pal>0.03, NA))

print(df_outliers_rm)

df <- df_outliers_rm %>%
  gather(key = "ROI", value = "proportion",bst_subic,subic_ant_thal,ncc_subic,subic_ext_glob_pal ) %>%
  convert_as_factor(Subjects, ROI)
print(df)

bxp <- ggboxplot(df, x = "ROI", y = "proportion", add = "point")
bxp

sumstats <- df %>%
  group_by(ROI) %>%
  get_summary_stats(proportion, type = "mean_sd")
print(sumstats)

# Check normal dist
normal <- df %>%
  group_by(ROI) %>%
  shapiro_test(proportion)
print(normal)


res.aov <- anova_test(data = df, dv = proportion, wid = Subjects, within = ROI)
get_anova_table(res.aov)

# pairwise comparisons
pwc <- df %>%
  pairwise_t_test(
    proportion ~ ROI, paired = TRUE,
    p.adjust.method = "fdr"
    )

pwc


