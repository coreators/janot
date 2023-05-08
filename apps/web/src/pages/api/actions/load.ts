import type { NextApiRequest, NextApiResponse } from "next";
import { loadDocuments } from "../../../lib/services/document-service";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  switch (req.method) {
    case "POST":
      handlePost();
      break;

    default:
      res.status(405).json({
        message: "Method not allowed",
      });
      break;
  }

  async function handlePost() {
    await loadDocuments();
    res.status(200).json({ success: true });
  }
}
