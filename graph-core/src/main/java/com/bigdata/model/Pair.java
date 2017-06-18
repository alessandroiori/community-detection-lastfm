package com.bigdata.model;

import java.io.Serializable;

public class Pair implements Serializable {
	
	private static final long serialVersionUID = 1L;
	private int id1;
	private int id2;
	private double similarity;
	
	public Pair(int id1, int id2, double similarity) {
		this.id1 = id1;
		this.id2 = id2;
		this.similarity = similarity;
	}
	
	public int getId1() {
		return id1;
	}
	
	public void setId1(int id1) {
		this.id1 = id1;
	}
	
	public int getId2() {
		return id2;
	}
	
	public void setId2(int id2) {
		this.id2 = id2;
	}
	
	public double getSimilarity() {
		return similarity;
	}
	
	public void setSimilarity(double similarity) {
		this.similarity = similarity;
	}
	
	@Override
	public String toString() {
		return this.id1 + "\t" + this.id2 +"\t"+ this.similarity;
	}

}
