// let name = prompt("你的名字是: ", "");
// // // while (name !== 'cc') {
// // //     name = prompt("您无权访问，请重新输入", "");
// // // }
function changeUser() {
    document.getElementById('user').innerHTML =  'Julius ,';
}

//八皇后
let count = 0;
function queen(a, cur) {
    if(cur === a.length) {
        console.log(a);
        count++;
        return;
    }
    for(let i = 0; i < a.length; i++) {
        a[cur] = i;
        let flag = true;
        for(let j = 0; j < cur; j++){
            let ab = i - a[j];
            if(a[j] === i || (ab > 0 ? ab : -ab) === cur - j) {
                flag = false;
                break;
            }
        }
        if(flag)
            queen(a,cur + 1);
    }
}

function changeAnswer() {
    document.getElementById('result').innerHTML =  count + "种不同的解";
    count = 0;
}

