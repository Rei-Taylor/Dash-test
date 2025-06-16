function getSpanningCellRenderer() {
    function SpanningCellRenderer() {}
    
    SpanningCellRenderer.prototype.init = function(params) {
        this.eGui = document.createElement('div');
        this.eGui.style.height = '100%';
        this.eGui.style.width = '100%';
        this.eGui.style.display = 'flex';
        this.eGui.style.alignItems = 'center';
        
        const rowSpan = params.data.Sr_No_rowSpan;
        if (rowSpan > 0) {
            this.eGui.innerHTML = params.value;
            this.eGui.style.backgroundColor = '#f5f5f5';
            this.eGui.rowSpan = rowSpan;
        } else {
            this.eGui.innerHTML = '';
        }
    };
    
    SpanningCellRenderer.prototype.getGui = function() {
        return this.eGui;
    };
    
    return SpanningCellRenderer;
}

var SpanningCellRenderer = getSpanningCellRenderer();
