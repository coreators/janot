import { PDFLoader } from "langchain/document_loaders/fs/pdf";
import { SupabaseVectorStore } from "langchain/vectorstores/supabase";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";
import { DirectoryLoader } from "langchain/document_loaders/fs/directory";

import { supabaseClient } from "../supabase/supabase-admin";

export const loadDocuments = async () => {
  const embeddings = new OpenAIEmbeddings();
  const loader = new DirectoryLoader("src/data", {
    ".pdf": (path) => new PDFLoader(path),
  });

  const docs = await loader.load();

  await supabaseClient.from("documents").delete().neq("id", 990102039);

  await SupabaseVectorStore.fromDocuments(docs, embeddings, {
    client: supabaseClient,
    tableName: "documents",
    queryName: "match_documents",
  });
};
