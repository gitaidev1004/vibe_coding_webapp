import { useRef, useState } from "react";
import { openDocument, saveHtmlFile } from "./fileio.js";
import "./App.css";

const FONT_SIZES = [10, 12, 14, 16, 18, 24, 32];

export default function App() {
  const editorRef = useRef(null);
  const fileInputRef = useRef(null);
  const [fontSize, setFontSize] = useState(14);
  const [fileName, setFileName] = useState("untitled.html");
  const [charCount, setCharCount] = useState(0);

  const updateCount = () => {
    setCharCount(editorRef.current.innerText.replace(/\n/g, "").length);
  };

  const applyFormat = (command) => {
    editorRef.current.focus();
    document.execCommand(command, false, null);
  };

  const handleNew = () => {
    if (!window.confirm("현재 내용을 지우고 새 문서를 만들까요?")) return;
    editorRef.current.innerHTML = "";
    setFileName("untitled.html");
    updateCount();
  };

  const handleOpen = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    try {
      editorRef.current.innerHTML = await openDocument(file);
      setFileName(file.name.replace(/\.[^.]+$/, "") + ".html");
      updateCount();
    } catch (error) {
      window.alert("파일을 열 수 없습니다: " + error.message);
    }
    event.target.value = "";
  };

  const handleSave = () => {
    saveHtmlFile(fileName, editorRef.current.innerHTML);
  };

  const handleKeyDown = (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s") {
      event.preventDefault();
      handleSave();
    }
  };

  // 버튼을 눌러도 편집기의 선택 영역이 해제되지 않게 한다.
  const keepSelection = (event) => event.preventDefault();

  return (
    <div className="app">
      <header className="toolbar">
        <button onMouseDown={keepSelection} onClick={handleNew}>새 문서</button>
        <button onMouseDown={keepSelection} onClick={() => fileInputRef.current.click()}>
          열기
        </button>
        <button onMouseDown={keepSelection} onClick={handleSave}>저장</button>
        <span className="divider" />
        <button className="b" onMouseDown={keepSelection} onClick={() => applyFormat("bold")}>
          B
        </button>
        <button className="i" onMouseDown={keepSelection} onClick={() => applyFormat("italic")}>
          I
        </button>
        <button className="u" onMouseDown={keepSelection} onClick={() => applyFormat("underline")}>
          U
        </button>
        <span className="divider" />
        <label>
          글자 크기
          <select value={fontSize} onChange={(e) => setFontSize(Number(e.target.value))}>
            {FONT_SIZES.map((size) => (
              <option key={size} value={size}>{size}px</option>
            ))}
          </select>
        </label>
        <input
          className="file-name"
          value={fileName}
          onChange={(e) => setFileName(e.target.value)}
          aria-label="파일 이름"
        />
        <input
          ref={fileInputRef}
          type="file"
          accept=".html,.htm,.txt"
          hidden
          onChange={handleOpen}
        />
      </header>
      <main className="page">
        <div
          ref={editorRef}
          className="editor"
          contentEditable
          suppressContentEditableWarning
          role="textbox"
          aria-multiline="true"
          style={{ fontSize: fontSize + "px" }}
          onInput={updateCount}
          onKeyDown={handleKeyDown}
        />
      </main>
      <footer className="status">
        {fileName} · 글자 수 {charCount} · 글자 크기 {fontSize}px
      </footer>
    </div>
  );
}
