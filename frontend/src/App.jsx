import './App.css'
import React from 'react'
import { useState } from 'react'
import YoutubeLogo from './components/YoutubeLogo';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

function App() {
  const [ytUrl, setYtUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);


  const handleClick = async () => {
    setLoading(true);

    try {
      const response = await fetch("https://youtube-in-seconds.onrender.com//summary", {
        method: "POST",
        headers: {"Content-Type" : "application/json"},
        body: JSON.stringify({url: ytUrl})
      });
      const data = await response.json();
      setSummary(data.summary);
      
    } catch (error) {
      console.log("Error in handle click");
    } finally {
      setLoading(false);
    }

  };

  const handleDownloadPDF = async () => {
    const input = document.getElementById('summary-content');
    if (!input) return;
  
    
    const originalWidth = input.style.width;
    input.style.width = '1200px'; 
  
    await new Promise((resolve) => setTimeout(resolve, 100)); 
  
    const canvas = await html2canvas(input, { scale: 2 });
    const imgData = canvas.toDataURL('image/png');
  
    const pdf = new jsPDF('p', 'mm', 'a4');
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const imgProps = pdf.getImageProperties(imgData);
    const imgHeight = (imgProps.height * pdfWidth) / imgProps.width;
  
    let heightLeft = imgHeight;
    let position = 0;
  
    pdf.addImage(imgData, 'PNG', 0, position, pdfWidth, imgHeight);
    heightLeft -= pdf.internal.pageSize.getHeight();
  
    while (heightLeft > 0) {
      position -= pdf.internal.pageSize.getHeight();
      pdf.addPage();
      pdf.addImage(imgData, 'PNG', 0, position, pdfWidth, imgHeight);
      heightLeft -= pdf.internal.pageSize.getHeight();
    }
  
    pdf.save('summary.pdf');
  
    // Reset width
    input.style.width = originalWidth;
  };
  
  
  

  return (
    <>
      <header className="relative text-center py-8 bg-white shadow">
        <h1 className="text-5xl font-bold text-gray-800">Youtube In Seconds</h1>
        <YoutubeLogo />
      </header>
  
      <main className="max-w-3xl mx-auto px-4 py-6">
        <div className="flex flex-col sm:flex-row gap-4 items-center mb-8">
          <input
            value={ytUrl}
            onChange={(e) => setYtUrl(e.target.value)}
            type="text"
            placeholder="Paste the YouTube URL here..."
            className="flex-grow w-full sm:w-auto px-4 py-3 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500"
          />
          <button
            onClick={handleClick}
            className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded shadow transition-colors"
          >
            {loading ? "Loading..." : "Summarize"}
          </button>
        </div>
  
        {summary && (
          <div className="bg-slate-100 p-6 rounded-lg shadow-lg">
           <div id="summary-content" className="prose prose-lg max-w-none">
        <div
          dangerouslySetInnerHTML={{
            __html: DOMPurify.sanitize(marked.parse(summary)),
          }}
        />
</div>
            <button
    onClick={handleDownloadPDF}
    className="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
  >
    Download as PDF
  </button>
          </div>
        )}
      </main>
    </>
  );
}

export default App
