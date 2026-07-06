import "./App.css";
import { Plus, Mic, ArrowUp, Image, Camera, FileText } from "lucide-react";
import { useState, useRef } from "react";

function App() {
  const [showMenu, setShowMenu] = useState(false);

  // File Picker References
const imageInputRef = useRef(null);
const fileInputRef = useRef(null);

// Open Image Picker
const openImagePicker = () => {
  if (imageInputRef.current) {
    imageInputRef.current.click();
  }
};

// Open File Picker
const openFilePicker = () => {
  if (fileInputRef.current) {
    fileInputRef.current.click();
  }
};

// Handle Image Selection
const [selectedFile, setSelectedFile] = useState(null);

const handleImage = (e) => {
  const file = e.target.files[0];

  if (file) {
    setSelectedFile(file);
  }
};

const handleFile = (e) => {
  const file = e.target.files[0];

  if (file) {
    setSelectedFile(file);
  }
};

  return (
    <div className="app">
      <div className="chat-area">
        <h1>🤖 Suri AI</h1>
        <p>How can I help you today?</p>
      </div>

      <div className="input-container">

  {selectedFile && (
    <div className="selected-file">
      📎 {selectedFile.name}
    </div>
  )}

  <div className="input-row">

    <div className="plus-container">


          <button
            className="icon-btn"
            onClick={() => setShowMenu(!showMenu)}
          >
            <Plus size={22} />
          </button>

          {showMenu && (
  <div className="popup-menu">

    <button onClick={openImagePicker}>
      <Image size={18} />
      Images
    </button>

    <button>
      <Camera size={18} />
      Camera
    </button>

    <button onClick={openFilePicker}>
      <FileText size={18} />
      Files
    </button>

  </div>
)}
        </div>



        <input
          type="text"
          placeholder="Ask anything..."
        />

        <button className="icon-btn">
          <Mic size={20} />
        </button>

        <button className="send-btn">
          <ArrowUp size={20} />
        </button>
      </div>
      </div>

<input
  type="file"
  accept="image/*"
  ref={imageInputRef}
  style={{ display: "none" }}
  onChange={handleImage}
/>

<input
  type="file"
  ref={fileInputRef}
  style={{ display: "none" }}
  onChange={handleFile}
/>

    </div>
  );
}

export default App;