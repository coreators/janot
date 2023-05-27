import type { NextApiRequest, NextApiResponse } from "next";
import fs from "fs";
import axios, { RawAxiosRequestHeaders } from "axios";
import formidable from "formidable";

export const config = {
  api: {
    bodyparser: false,
  },
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === "POST") {
    const form = formidable();

    console.log("parsing form");
    try {
      form.parse(req, async (err, fields, files) => {
        console.log("form parsed");
        if (err) {
          console.error(err);
          res.status(500).json({ error: "Error processing file upload" });
          return;
        }

        // Access the received blob via files.audioData.path
        const audioFile = Array.isArray(files.audioData)
          ? files.audioData[0]
          : files.audioData;
        const audioData = fs.readFileSync(audioFile.filepath);
        const audioBlob = new Blob([audioData]);

        const model = fields.model;

        const body = new FormData();

        body.append("file", audioBlob);
        body.append("model", model as string);

        const headers: RawAxiosRequestHeaders = {};
        headers["Content-Type"] = "multipart/form-data";
        if (process.env.OPENAI_API_KEY) {
          headers["Authorization"] = `Bearer ${process.env.OPENAI_API_KEY}`;
        }
        const response = await axios.post(
          whisperApiEndpoint + "transcriptions",
          body,
          {
            headers,
          }
        );
        console.log(response.data);

        // Return the response
        res.json({ text: "Transcription result" });
      });
    } catch (e) {
      console.error("Error uploading file:", e);
      res.status(500).json({ error: "File upload failed" });
    }
  } else {
    res.status(405).json({ error: "Method Not Allowed" });
  }
}

export const whisperApiEndpoint = "https://api.openai.com/v1/audio/";
