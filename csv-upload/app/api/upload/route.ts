import { handleUpload, type HandleUploadBody } from "@vercel/blob/client"
import { NextResponse } from "next/server"

export async function POST(request: Request): Promise<NextResponse> {
  const body = (await request.json()) as HandleUploadBody

  try {
    const jsonResponse = await handleUpload({
      body,
      request,
      onBeforeGenerateToken: async (pathname) => {
        // This is where you could check auth if needed
        return {
          allowedContentTypes: ["text/csv"],
          tokenPayload: JSON.stringify({
            // optional, sent to your server on upload completion
          }),
        }
      },
      onUploadCompleted: async ({ blob, tokenPayload }) => {
        // This is called after the file is uploaded to Vercel Blob
        console.log("blob upload completed", blob, tokenPayload)
        // You could save the blob.url to your database here
      },
    })

    return NextResponse.json(jsonResponse)
  } catch (error) {
    return NextResponse.json({ error: (error as Error).message }, { status: 400 })
  }
}

