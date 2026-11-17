import React from "react";

function ModelColumn({modelName, answer}) {
    return(
        <div>
            <h3>{modelName}</h3>
            <p>{answer}</p>
        </div>
    )
}

export default ModelColumn;