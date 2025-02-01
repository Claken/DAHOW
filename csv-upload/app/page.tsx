"use client"

import { useState } from "react"
import { upload } from "@vercel/blob/client"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { motion } from "framer-motion"
import { FileUp, CheckCircle, Droplets, MessageSquare } from "lucide-react"

export default function CSVUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [prompt, setPrompt] = useState<string>("")
  const [uploading, setUploading] = useState(false)
  const [uploadedUrl, setUploadedUrl] = useState<string | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0])
    }
  }

  const handlePromptChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setPrompt(e.target.value)
  }

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    try {
      const newBlob = await upload(file.name, file, {
        access: "public",
        handleUploadUrl: "/api/upload",
      })
      setUploadedUrl(newBlob.url)

      if (prompt) {
        console.log("Prompt to be sent:", prompt)
        // Implement your API call to send the prompt here
      }
    } catch (error) {
      console.error("Upload failed:", error)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-400 via-blue-500 to-cyan-500 p-4">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        <Card className="backdrop-blur-lg bg-white/20 shadow-xl border border-white/30">
          <CardHeader>
            <div className="flex items-center justify-center mb-2">
              <Droplets className="w-10 h-10 text-blue-100" />
            </div>
            <CardTitle className="text-4xl font-bold text-white text-center tracking-wider">DAHOW</CardTitle>
            <CardDescription className="text-blue-100 text-center">
              Upload your .csv file and optional prompt
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="relative">
              <Input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                disabled={uploading}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="flex items-center justify-center w-full px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md cursor-pointer hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
              >
                <FileUp className="w-5 h-5 mr-2" />
                Choose CSV File
              </label>
            </div>
            {file && (
              <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-sm text-blue-100">
                Selected file: {file.name}
              </motion.p>
            )}
            <div className="relative">
              <Textarea
                placeholder="Enter optional prompt here..."
                value={prompt}
                onChange={handlePromptChange}
                className="w-full p-2 text-sm text-blue-900 bg-white/50 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-blue-300"
                rows={3}
              />
              <MessageSquare className="absolute right-2 top-2 w-5 h-5 text-blue-400" />
            </div>
          </CardContent>
          <CardFooter>
            <Button
              onClick={handleUpload}
              disabled={!file || uploading}
              className="w-full bg-cyan-600 hover:bg-cyan-700 text-white transition-colors duration-200"
            >
              {uploading ? "Uploading..." : "Upload CSV & Prompt"}
            </Button>
          </CardFooter>
        </Card>
        {uploadedUrl && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mt-4 text-center">
            <div className="inline-flex items-center px-4 py-2 bg-green-500 text-white rounded-full shadow-lg">
              <CheckCircle className="w-5 h-5 mr-2" />
              File uploaded successfully!
            </div>
            <a
              href={uploadedUrl}
              className="block mt-2 text-blue-100 hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              View uploaded file
            </a>
          </motion.div>
        )}
      </motion.div>
    </div>
  )
}

