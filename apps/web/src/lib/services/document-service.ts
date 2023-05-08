import { PDFLoader } from "langchain/document_loaders/fs/pdf";
import { SupabaseVectorStore } from "langchain/vectorstores/supabase";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";

import { supabaseClient } from "../supabase/supabase-admin";

export const loadAndSearch = async () => {
  const embeddings = new OpenAIEmbeddings();
  const loader = new PDFLoader("src/data/Jaeyoun_s_CV.pdf");
  const docs = await loader.load();

  const vectorStore = await SupabaseVectorStore.fromDocuments(
    docs,
    embeddings,
    {
      client: supabaseClient,
      tableName: "documents",
      queryName: "match_documents",
    }
  );

  // Search for the most similar document
  const resultOne = await vectorStore.similaritySearch("Project", 1);
  console.log(resultOne);
  return resultOne;
};
