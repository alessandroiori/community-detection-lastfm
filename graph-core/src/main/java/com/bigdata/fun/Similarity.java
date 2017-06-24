package com.bigdata.fun;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.mllib.linalg.SparseVector;
import org.apache.spark.mllib.linalg.Vector;
import org.apache.spark.mllib.linalg.Vectors;
import org.apache.spark.mllib.linalg.distributed.CoordinateMatrix;
import org.apache.spark.mllib.linalg.distributed.IndexedRowMatrix;
import org.apache.spark.mllib.linalg.distributed.RowMatrix;

import com.bigdata.dao.DAOFactory;
import com.bigdata.model.Listening;
import com.bigdata.model.Pair;
import com.bigdata.model.UserRating;

import scala.Tuple2;



public class Similarity implements Serializable, FirstPhase, SecondPhase {

	private static final long serialVersionUID = 1L;
	private Double threshould;


	public JavaRDD<Pair> run(JavaSparkContext sc, DAOFactory input) {

		JavaRDD<Listening> listenings = input
				.getListeningDAO()
				.getAll(sc, Listening.class);

		int totalNumberOfUser = listenings.max(new DummyComp()).getUserid().intValue()+1;
		System.out.println(totalNumberOfUser);
		JavaPairRDD<Integer, UserRating> pair = listenings.mapToPair(r-> {
			return new Tuple2<Integer, UserRating>(r.getArtistid().intValue(), 
					new UserRating(r.getUserid().intValue(), r.getListenings().doubleValue()));
		});

		JavaRDD<Vector> rows = pair.groupByKey()
				.map(p -> {
					List<Tuple2<Integer,Double>> list = new ArrayList<>();

					for (UserRating userRating : p._2) {
						list.add(new Tuple2<>(userRating.getUserId(), userRating.getRating()));
					}
					return Vectors.sparse(totalNumberOfUser, list);
				});
		RowMatrix mat = new RowMatrix(rows.rdd());

		CoordinateMatrix matr = mat.columnSimilarities();
		IndexedRowMatrix imat = matr.toIndexedRowMatrix();
		JavaPairRDD<Integer,UserRating> pair1 = imat.rows().toJavaRDD().flatMapToPair(p -> {
			int index = (int) p.index();
			SparseVector vector = (SparseVector) p.vector();
			int[] indices = vector.indices();
			double[] values = vector.values();
			List<Tuple2<Integer, UserRating>> list = new ArrayList<>();	
			for (int i = 0; i < indices.length; i++) {
				list.add(new Tuple2<Integer, UserRating>(index, new UserRating(indices[i], values[i])));
			}
			return list.iterator();
		});
		JavaPairRDD<Integer,UserRating> filter = pair1.filter(f -> {
			return f._2().getRating() >= this.threshould;
		}); 

		return filter.map(f -> {
			return new Pair(f._1, f._2.getUserId(), f._2.getRating());
		});

	}


	public void setThreshould(Double thres) {
		this.threshould = thres;
	}


	@Override
	public JavaRDD<Pair> run(JavaRDD<Pair> rdd) {
		return rdd;
	}

	class DummyComp implements Comparator<Listening>, Serializable {

		private static final long serialVersionUID = 1L;

		@Override
		public int compare(Listening o1, Listening o2) {
			return (int) (o1.getUserid() - o2.getUserid());
		}

	}

}
