package com.bigdata.main;


import com.bigdata.fun.IService;


public class Main {
		
	public static void main(String[] args) {
		
		Double thres = Double.parseDouble(args[0].toLowerCase());
		
		String yml = args[1];
		
		IService fun = MyContext.getInstance().getService(yml, thres); 
		
		fun.run();
			
		
		
	}

}
