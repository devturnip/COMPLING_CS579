import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.util.CoreMap;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.apache.pdfbox.text.PDFTextStripperByArea;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;


import java.io.File;
import java.io.IOException;

public class rbparse {
    public static void main(String[] args) {
        try {

            PDDocument pdf = PDDocument.load(new File("2007_puget_sound.pdf"));

            PDFTextStripperByArea pdfTextStripperByArea = new PDFTextStripperByArea();
            pdfTextStripperByArea.setSortByPosition(true);

            PDFTextStripper tStripper = new PDFTextStripper();

            String pdfFileInText = tStripper.getText(pdf);
            System.out.println(pdfFileInText);

            pdf.close();
            } catch (IOException ex) {
            ex.printStackTrace();
        }

        /*Properties props = new Properties();

        props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");

        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

        // read some text in the text variable
        String text = "She went to America last week.";

        // create an empty Annotation just with the given text
        Annotation document = new Annotation(text);

        // run all Annotators on this text
        pipeline.annotate(document);

        System.out.println( "End of Processing" );
        List<CoreMap> sentences = document.get(CoreAnnotations.SentencesAnnotation.class);

        List<String> words = new ArrayList<>();
        List<String> posTags = new ArrayList<>();
        List<String> nerTags = new ArrayList<>();
        for (CoreMap sentence : sentences) {
            // traversing the words in the current sentence
            for (CoreLabel token : sentence.get(CoreAnnotations.TokensAnnotation.class)) {
                // this is the text of the token
                String word = token.get(CoreAnnotations.TextAnnotation.class);
                words.add(word);
                // this is the POS tag of the token
                String pos = token.get(CoreAnnotations.PartOfSpeechAnnotation.class);
                posTags.add(pos);
                // this is the NER label of the token
                String ne = token.get(CoreAnnotations.NamedEntityTagAnnotation.class);
                nerTags.add(ne);
            }
        }

        System.out.println(words.toString());
        System.out.println(posTags.toString());
        System.out.println(nerTags.toString());
        */
    }
}
