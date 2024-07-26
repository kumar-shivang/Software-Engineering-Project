import React, { useState } from 'react';
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-javascript';  // Import desired language mode
import 'ace-builds/src-noconflict/theme-github';     // Import desired theme


import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/ext-language_tools"

const CodeEditor = () => {
    const [code, setCode] = useState('// Write your code here');


    function onChange(newValue) {
        console.log("change", newValue)
      }

    return (
        <div className="p-4">
        <h2 className="text-2xl font-bold mb-4">Python Assignment</h2>
        <AceEditor
                mode="python"
                theme="github"
                onChange={onChange}
                name="UNIQUE_ID_OF_DIV"
                editorProps={{ $blockScrolling: true }}
                setOptions={{
                  enableBasicAutocompletion: true,
                  enableLiveAutocompletion: true,
                  enableSnippets: true
                }}
            />
              <button className="fixed bottom-5 right-10 bg-blue-500 text-white p-3 rounded-md shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300 focus:ring-opacity-75">
                Submit
            </button>
        </div>
    );
};

export default CodeEditor;
