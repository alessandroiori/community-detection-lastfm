package com.bigdata.model;

import java.io.Serializable;

public class Tag implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	private Long tagId;
	
	private String tagValue;

	public Long getTagid() {
		return tagId;
	}

	public void setTagid(Long tagId) {
		this.tagId = tagId;
	}

	public String getTagvalue() {
		return tagValue;
	}

	public void setTagvalue(String tagValue) {
		this.tagValue = tagValue;
	}
	
	@Override
	public String toString() {
		return this.tagId + "\t" + this.tagValue;
	}

}
