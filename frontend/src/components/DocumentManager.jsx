import { useState, useEffect } from 'react'
import { uploadDocument, listDocuments, deleteDocument, reindexDocuments } from '../services/api'

function DocumentManager({ onUpdate }) {
  const [documents, setDocuments] = useState([])
  const [stats, setStats] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [reindexing, setReindexing] = useState(false)
  const [uploadStatus, setUploadStatus] = useState(null)

  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    try {
      const response = await listDocuments()
      setDocuments(response.documents || [])
      setStats(response.stats || null)
    } catch (error) {
      console.error('Error loading documents:', error)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    // Check file type
    const allowedTypes = ['.pdf', '.docx', '.doc', '.txt']
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase()
    
    if (!allowedTypes.includes(fileExtension)) {
      setUploadStatus({
        type: 'error',
        message: `Unsupported file type. Allowed types: ${allowedTypes.join(', ')}`,
      })
      return
    }

    setUploading(true)
    setUploadStatus(null)

    try {
      const response = await uploadDocument(file)
      if (response.already_exists) {
        setUploadStatus({
          type: 'info',
          message: `Document "${response.filename}" already exists in database (${response.chunks} chunks).`,
        })
      } else {
        const statsMsg = response.database_stats 
          ? ` Database now has ${response.database_stats.total_documents} documents with ${response.database_stats.total_chunks} total chunks.`
          : ''
        setUploadStatus({
          type: 'success',
          message: `Document "${response.filename}" added to database! ${response.chunks} chunks created.${statsMsg}`,
        })
      }
      await loadDocuments()
      if (onUpdate) onUpdate()
      
      // Clear file input
      e.target.value = ''
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.detail || error.message || 'Failed to upload document',
      })
    } finally {
      setUploading(false)
    }
  }

  const handleDelete = async (documentId) => {
    if (!confirm('Are you sure you want to delete this document?')) return

    try {
      await deleteDocument(documentId)
      await loadDocuments()
      if (onUpdate) onUpdate()
      setUploadStatus({
        type: 'success',
        message: 'Document deleted successfully',
      })
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.detail || error.message || 'Failed to delete document',
      })
    }
  }

  const handleReindex = async () => {
    setReindexing(true)
    setUploadStatus(null)

    try {
      const response = await reindexDocuments()
      setUploadStatus({
        type: 'success',
        message: `Reindexed ${response.count} documents successfully`,
      })
      await loadDocuments()
      if (onUpdate) onUpdate()
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.detail || error.message || 'Failed to reindex documents',
      })
    } finally {
      setReindexing(false)
    }
  }

  return (
    <div className="card bg-base-100 shadow-xl">
      <div className="card-body">
        <h2 className="card-title">Document Management</h2>

        {uploadStatus && (
          <div
            className={`alert ${
              uploadStatus.type === 'success' 
                ? 'alert-success' 
                : uploadStatus.type === 'info'
                ? 'alert-info'
                : 'alert-error'
            }`}
          >
            <span>{uploadStatus.message}</span>
          </div>
        )}

        <div className="divider">Upload Documents</div>

        <div className="form-control">
          <label className="label">
            <span className="label-text">Upload PDF, DOCX, or TXT files</span>
          </label>
          <input
            type="file"
            className="file-input file-input-bordered w-full"
            accept=".pdf,.docx,.doc,.txt"
            onChange={handleFileUpload}
            disabled={uploading}
          />
          {uploading && (
            <div className="mt-2">
              <span className="loading loading-spinner loading-sm"></span>
              <span className="ml-2">Processing document...</span>
            </div>
          )}
        </div>

        <div className="divider">Manage Documents</div>

        {stats && (
          <div className="stats stats-vertical lg:stats-horizontal shadow mb-4">
            <div className="stat">
              <div className="stat-title">Total Documents</div>
              <div className="stat-value text-primary">{stats.total_documents}</div>
            </div>
            <div className="stat">
              <div className="stat-title">Total Chunks</div>
              <div className="stat-value text-secondary">{stats.total_chunks}</div>
            </div>
            <div className="stat">
              <div className="stat-title">Database Size</div>
              <div className="stat-value text-accent">{stats.total_size_mb} MB</div>
            </div>
          </div>
        )}

        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Processed Documents ({documents.length})</h3>
          <button
            className="btn btn-sm btn-outline"
            onClick={handleReindex}
            disabled={reindexing}
          >
            {reindexing ? (
              <>
                <span className="loading loading-spinner loading-sm"></span>
                Reindexing...
              </>
            ) : (
              'Reindex All'
            )}
          </button>
        </div>

        {documents.length === 0 ? (
          <div className="text-center py-8 text-base-content/60">
            <p>No documents uploaded yet.</p>
            <p className="text-sm mt-2">Upload documents above to enable document-based chat.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="table table-zebra">
              <thead>
                <tr>
                  <th>Filename</th>
                  <th>Chunks</th>
                  <th>Size</th>
                  <th>Uploaded</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {documents.map((doc) => (
                  <tr key={doc.document_id}>
                    <td>{doc.filename}</td>
                    <td>{doc.chunks}</td>
                    <td>{(doc.file_size / 1024).toFixed(1)} KB</td>
                    <td>{doc.uploaded_at ? new Date(doc.uploaded_at).toLocaleDateString() : 'Unknown'}</td>
                    <td>
                      <button
                        className="btn btn-sm btn-error"
                        onClick={() => handleDelete(doc.document_id)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default DocumentManager

