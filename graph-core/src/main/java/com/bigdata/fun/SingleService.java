package com.bigdata.fun;

import java.io.File;
import java.io.IOException;

import org.apache.commons.io.FileUtils;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

import com.bigdata.dao.DAOFactory;
import com.bigdata.model.Pair;

public class SingleService implements IService{
	private static final String DELIMITER = "\t";
	private final static String tmp_path = "tmp";
	private FirstPhase first;
	private SecondPhase second;	
	private DAOFactory input;
	private DAOFactory output;
	
	public void run() {
			
		JavaSparkContext scIn = input.createContext();
		
		JavaRDD<Pair> obj = second.run(first.run(scIn, input));
		obj.saveAsTextFile(tmp_path);
		scIn.stop();
		scIn.close();
		
		JavaSparkContext scOut = output.createContext();
		JavaRDD<String> lines = scOut.textFile(tmp_path+"/part-00*");
		JavaRDD<Pair> object = lines.map(f -> {
			String[] s = f.split(DELIMITER);
			
			return new Pair(Integer.parseInt(s[0]), Integer.parseInt(s[1]), Double.parseDouble(s[2]));
		});
		output.getPairDAO().update(object);
		scOut.stop();
		scOut.close();
		try {
			FileUtils.deleteDirectory(new File(tmp_path));
		} catch (IOException e) {

			e.printStackTrace();
		}
	}
	
	
	
	public void setInput(DAOFactory input) {
		this.input = input;
	}
	
	public void setOutput(DAOFactory output) {
		this.output = output;
	}
	
	public void setSecond(SecondPhase second) {
		this.second = second;
	}

	public void setFirst(FirstPhase first) {
		this.first = first;
	}
}
