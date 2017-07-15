package com.bigdata.model;

import java.io.Serializable;

public class UserRating implements Serializable  {
	
	private static final long serialVersionUID = 1L;
	private int userId;
	private double rating;
	public UserRating() {
		
	}
	
	public UserRating(int userId, double rating) {
		this.userId = userId;
		this.rating = rating;
	}
	public double getRating() {
		return rating;
	}
	public void setRating(double rating) {
		this.rating = rating;
	}
	public int getUserId() {
		return userId;
	}
	public void setUserId(int userId) {
		this.userId = userId;
	}
	
	@Override
	public String toString() {
		return this.userId + "\t" + this.rating;
	}
	
	
}
