package com.bigdata.model;

import java.io.Serializable;

public class User implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private Long userId;
	
	
	
	public Long getUserid() {
		return userId;
	}
	
	public void setUserid(Long userId) {
		this.userId = userId;
	}
	
	@Override
	public String toString() {
		return this.userId.toString();
	}

}
