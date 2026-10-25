try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $docPath = 'd:\trienkhaihethong\report\BAO_CAO_CUOI_KY.docx'
    $doc = $word.Documents.Open($docPath, $false, $true)
    
    # wdStatisticPages = 2, wdStatisticWords = 0, wdStatisticParagraphs = 4
    $pageCount = $doc.ComputeStatistics(2)
    $words = $doc.ComputeStatistics(0)
    $paragraphs = $doc.ComputeStatistics(4)
    
    Write-Output "=== MICROSOFT WORD VERIFICATION RESULT ==="
    Write-Output "Exact Page Count: $pageCount"
    Write-Output "Exact Word Count: $words"
    Write-Output "Exact Paragraph Count: $paragraphs"
    
    $doc.Close([ref]$false)
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
} catch {
    Write-Output "Error using Word COM: $($_.Exception.Message)"
}
