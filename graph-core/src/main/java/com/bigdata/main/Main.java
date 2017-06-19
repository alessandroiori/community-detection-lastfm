package com.bigdata.main;


import com.bigdata.fun.TemplateMethod;


public class Main {
		
	public static void main(String[] args) {
		
		Double thres = Double.parseDouble(args[0].toLowerCase());
		
		TemplateMethod fun = MyContext.getInstance().getSimilarity(thres); 
		
		fun.run();
			
		
		
	}

}
