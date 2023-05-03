// 取得學號
//stuID = $('.user_no.truncate-text').text()

mainTable = $('.activity-body.sync-scroll')
//idSpan = mainTable.find(`[tipsy="submission.student.user_no"][original-title="408000445"]`)
//row = idSpan.parents(`li.homework-row:first`)
//scoreInput = row.find(`input[type="text"].score-input`)

sleep = function (ms = 500) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

eventClick = new Event("blur");


main = async function () {
    stuIDList = Object.keys(scores)

    for (let i = 0; i < stuIDList.length; i++) {
        console.log(`${i}/${stuIDList.length}`)
        
        stuID = stuIDList[i]

        let score = scores[stuID]
  
        let idSpan = mainTable.find(`[tipsy="submission.student.user_no"][original-title="${stuID}"]`)
        let row = idSpan.parents(`li.homework-row:first`)
        let scoreInput = row.find(`input[type="text"].score-input`)
        // scoreInput.focus().val(score).blur().change()
        scoreInput.val(score)
        // scoreInput.val(score).change()
        let scoreInputEle = scoreInput[0]
        scoreInputEle.dispatchEvent(eventClick)
        
        await sleep(100)
    }   
}

main()
