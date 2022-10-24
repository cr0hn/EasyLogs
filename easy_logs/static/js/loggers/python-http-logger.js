function newPythonHTTPLoggerEntry(logEntry, target, maxEntriesPerList) {

    // Select color from log level
    let color = 'text-dark';

    switch (logEntry.log_level_name) {
        case 'DEBUG':
            color = 'text-info';
            break;
        case 'INFO':
            color = 'text-success';
            break;
        case 'WARNING':
            color = 'text-warning';
            break;
        case 'ERROR':
            color = 'text-danger';
            break;
        case 'CRITICAL':
            color = 'text-danger';
            break;
        default:
            color = 'text-dark';
    }

    // Random Log Table Id for the table
    const randomTableId = Math.floor(Math.random() * 100000000);

    const entry = $(`
<div id="logsTable${randomTableId}" onclick="changeIcon('#logsTable${randomTableId}');" class="row mb-1 card shadow display-none" data-toggle="collapse" data-target="#logDetails${randomTableId}" aria-expanded="false" aria-controls="collapse">
    <div class="col-sm-12 m-2">
        <i class="float-left fas fa-caret-right"></i>
        <div class="row bb-1">
            <div class="col-lg-1 col-3 text-xsm text-center font-weight-bold ${color} text-uppercase border-right-log align-middle" style="border-right: 1px solid #0d5aa7">${logEntry.log_level_name}</div>
            <div class="col-lg-2 col-3 text-xsm text-center border-right-log align-middle">${logEntry.logger_name}</div>
            <div class="col-lg-3 col-3 text-xsm text-center border-right-log align-middle">${logEntry.created}</div>
            <div class="col-lg-6 col-3 text-xsm align-middle">${logEntry.log_message}</div>
        </div>
    </div>
</div>    
<div class="row collapse" id="logDetails${randomTableId}">
    <div class="card card-body mb-2 row-payload">
        <pre class="p-0 m-0">
            <code id="logsCodeTable${randomTableId}" class="language-json m-0 p-0 pr-2">
${JSON.stringify(logEntry.payload, null, 2)}</code>
        </pre>
    </div>
</div>
    `)

    // Append to target
    target.prepend(entry);

    $(`#logsTable${randomTableId}`).show(200);

    // Highlight the new entry
    hljs.highlightElement(document.getElementById(`logsCodeTable${randomTableId}`));

    // Remove old entries
    if (target.children('[id^="logsTable"]').length > maxEntriesPerList) {
        target.children('[id^="logsTable"]').last().hide("slow", function () {
            $(this).remove();
        });
    }
}
