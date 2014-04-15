ggplot(var.search, aes(K,LR)) + 
	facet_grid(. ~ T) +
	geom_boxplot() +
	geom_jitter(alpha=1/3,position=position_jitter(width=.05)) +
	theme_bw() +
	labs(x="K",y="Likelihood ratio vs controls only model") +
	scale_x_discrete(limits=c("K50","K100","K200","K300","K400","K500","K600","K700")) +
	geom_hline(yintercept=5.99) +
	geom_hline(yintercept=4.61,linetype="dashed") + 
	theme(axis.text.x = element_text(angle=90,hjust=1))
	
ggplot(var.search, aes(K,UpperSq)) + 
	facet_grid(. ~ T) +
	geom_boxplot() +
	geom_jitter(alpha=1/3,position=position_jitter(width=.05)) +
	theme_bw() +
	labs(x="K",y="95% lower limit for Variety") +
	scale_x_discrete(limits=c("K50","K100","K200","K300","K400","K500","K600","K700")) +
	geom_hline(yintercept=0) +
	theme(axis.text.x = element_text(angle=90,hjust=1))