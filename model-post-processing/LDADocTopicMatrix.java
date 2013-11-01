/*
Reads in the mallet LDA doc composition output and spits out a doc by topic weight matrix. 
Currently assumes that the first line of the standard mallet LDA output file (i.e., the header) has been removed
*/

import java.io.*;
import java.util.*;
import java.lang.*;

public class LDADocTopicMatrix
{
	public static void main (String [] args) throws Exception
	{
		BufferedReader infile = new BufferedReader(new FileReader(args[0])); // unordered LDA output
		PrintWriter outfile = new PrintWriter (args[1]); // ordered LDA output file
		Map <String,String> weights = new HashMap <String,String>();
		final int numTopics = Integer.parseInt(args[2]);
		int counter = 0;
		
		// print header for output file
		outfile.print("filename\t");
		for(int k = 0; k < numTopics; ++k)
			outfile.print(k + "\t");
		outfile.print("\n");
		
		while(infile.ready())
		{
			String temp = infile.readLine(); 
			String [] doc = temp.split("\t"); // split the line based on the tab separator
			outfile.print(doc[1] + "\t");
			
			// walk through the string array to get the topic-weight mappings
			for(int i = 2; i < doc.length; i+=2)
				weights.put(doc[i],doc[i+1]);
			
			for(int i = 0; i < numTopics; ++i)
			{
				String key = Integer.toString(i);
				outfile.print(weights.get(key) + "\t");
			}
			outfile.print("\n");
			counter++;
			//System.out.println(weights.toString());
			weights.clear(); // refresh the hashmap for the next round
		}
		outfile.close();
		System.out.println("Success! " + counter + " docs processed."); // report!	
	}
}
