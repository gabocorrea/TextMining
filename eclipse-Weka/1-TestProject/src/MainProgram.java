
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Random;

import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.core.Instances;

public class MainProgram {
	
	public static void main(String[] args) throws Exception {
		System.out.println("MainProgram has started\n");
		
		
		BufferedReader breader = null;
		breader = new BufferedReader(new FileReader("C:\\Users\\gabo\\Documents\\U\\F\\TextMining\\textMining01.csv_balanced_StringToWordVector-applied.arff"));
		
		Instances data_train = new Instances(breader);
		data_train.setClassIndex(data_train.numAttributes()-1);
		
		breader.close();
		
		
		
		BufferedReader breader2 = null;
		breader2 = new BufferedReader(new FileReader("C:\\Users\\gabo\\Documents\\U\\F\\TextMining\\textMining01.csv-testSet.arff"));
		
		Instances data_test = new Instances(breader2);
		breader2.close();
		
		
		Classifier nB = new weka.classifiers.bayes.NaiveBayes();
		nB.buildClassifier(data_train);
		Evaluation eval = new Evaluation(data_train);
		eval.crossValidateModel(nB, data_train, 10, new Random(1), new Object[] {});
		//System.out.println(nB);
		System.out.println(eval.toSummaryString("\nResults\n======\n", true));
		System.out.println(eval.toClassDetailsString());
		System.out.println(eval.toMatrixString());
	}
	
}
