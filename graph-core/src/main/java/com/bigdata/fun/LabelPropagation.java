package com.bigdata.fun;

import java.util.ArrayList;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.graphframes.GraphFrame;

import com.bigdata.model.Pair;

	
public class LabelPropagation implements SecondPhase {

	@Override
	public JavaRDD<Pair> run(JavaRDD<Pair> rdd) {
		SparkSession spark = new SparkSession(rdd.context());
		
		Dataset<Row> df = spark.createDataFrame(rdd, Pair.class);
		
		Dataset<Row> vx = spark.createDataFrame(rdd.flatMap(f -> {
			java.util.List<Integer> l = new ArrayList<Integer>(2);
			l.add(f.getId1());
			l.add(f.getId2());
			return l.iterator();
		}).distinct(), Integer.class);
		
		GraphFrame gf = new GraphFrame(vx, df);
		
		org.graphframes.lib.LabelPropagation lp = gf.labelPropagation().maxIter(4);
		Dataset<Row> ed = lp.run();
		return rdd;
	}

}
