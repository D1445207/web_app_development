let calculationHistory = [];

document.addEventListener('DOMContentLoaded', () => {
    // 1. Fetch available years to populate select dropdowns
    fetch('/api/years')
        .then(res => res.json())
        .then(data => {
            const originalSelect = document.getElementById('original_year');
            const targetSelect = document.getElementById('target_year');
            
            data.years.forEach(year => {
                const opt1 = document.createElement('option');
                opt1.value = year;
                opt1.textContent = `${year} 年`;
                originalSelect.appendChild(opt1);
                
                const opt2 = document.createElement('option');
                opt2.value = year;
                opt2.textContent = `${year} 年`;
                targetSelect.appendChild(opt2);
            });
            
            // Set default selections (earliest to latest)
            if (data.years.length >= 2) {
                originalSelect.value = data.years[0];
                targetSelect.value = data.years[data.years.length - 1];
            }
        })
        .catch(err => console.error("Error fetching years:", err));

    // 2. Handle calculation submission
    const calcBtn = document.getElementById('calculateBtn');
    calcBtn.addEventListener('click', () => {
        const originalYear = document.getElementById('original_year').value;
        const targetYear = document.getElementById('target_year').value;
        const amount = document.getElementById('amount').value;
        
        if (!amount || amount <= 0) {
            alert('請輸入有效的金額');
            return;
        }

        calcBtn.textContent = '計算中...';
        calcBtn.disabled = true;

        fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start_year: originalYear,
                end_year: targetYear,
                amount: amount
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            
            // Show result area
            const resultArea = document.getElementById('resultArea');
            resultArea.style.display = 'block';
            
            // Update values
            document.getElementById('targetAmountDisplay').textContent = data.real_value.toLocaleString('en-US');
            document.getElementById('bigMacCount').textContent = data.big_mac_count;
            document.getElementById('porkBentoCount').textContent = data.pork_bento_count;
            
            // Trigger fade-in animation
            resultArea.classList.remove('fade-in');
            void resultArea.offsetWidth; // trigger DOM reflow
            resultArea.classList.add('fade-in');
            
            // 3. Update history (F-03)
            addToHistory({
                originalYear: originalYear,
                targetYear: targetYear,
                originalAmount: amount,
                targetAmount: data.real_value
            });
        })
        .catch(err => {
            console.error('Error during calculation:', err);
            alert('計算過程發生錯誤，請稍後再試。');
        })
        .finally(() => {
            calcBtn.textContent = '開始計算';
            calcBtn.disabled = false;
        });
    });
});

// Function to manage history list
function addToHistory(record) {
    // Add to beginning of array
    calculationHistory.unshift(record);
    
    // Keep only the last 5 records
    if (calculationHistory.length > 5) {
        calculationHistory.pop();
    }
    
    const historyArea = document.getElementById('historyArea');
    const historyList = document.getElementById('historyList');
    
    historyArea.style.display = 'block';
    historyList.innerHTML = '';
    
    calculationHistory.forEach((item, index) => {
        const li = document.createElement('li');
        li.className = 'history-item fade-in';
        li.style.animationDelay = `${index * 0.1}s`;
        
        li.innerHTML = `
            <div class="history-info">
                <span class="history-years">${item.originalYear} 年 ➔ ${item.targetYear} 年</span>
                <span class="history-original">原始：NT$ ${parseFloat(item.originalAmount).toLocaleString('en-US')}</span>
            </div>
            <div class="history-target">NT$ ${item.targetAmount.toLocaleString('en-US')}</div>
        `;
        historyList.appendChild(li);
    });
}
