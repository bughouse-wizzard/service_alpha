# Тестовый код фронтенда системы поиска контрактов по КТРУ

## Содержание (только тесты)
1. [test_block.html](#testblockhtml)
2. [test_direct_response.html](#testdirectresponsehtml)
3. [test_frontend.html](#testfrontendhtml)
4. [test_interface.html](#testinterfacehtml)
5. [test_response.html](#testresponsehtml)

---

### Файл: `test_block.html`
```html
<div class="search-registry-entry-block box-shadow-search-input">
<div class="row no-gutters registry-entry__form mr-0">
<div class="col-8 pr-0">
<div class="registry-entry__header">
<div class="row registry-entry__header-top m-0">
<div class="col p-0 d-flex">
<div class="col-9 p-0 registry-entry__header-top__title text-truncate">
                                   223-ФЗ
                                   Прочие
                                    
                                </div>
<div class="w-space-nowrap ml-auto registry-entry__header-top__icon">
<a class="distancedText newExternalPopUpLink" href="https://zakupki.gov.ru/223/purchase/public/download/signs/render-pf.html?id=72293346&amp;modal=true" shablon-pattern="223FZModal">
<img alt="" src="/epz/static/img/icons/icon_key.svg"/>
</a>
<a class="m-0" href="https://zakupki.gov.ru/223/purchase/public/print-form/show.html?pfid=72293346" target="_blank">
<img alt="" src="/epz/static/img/icons/icon_print_small.svg"/>
</a>
</div>
</div>
</div>
<div class="d-flex registry-entry__header-mid align-items-center">
<div class="registry-entry__header-mid__number">
<a href="/epz/order/notice/notice223/common-info.html?noticeInfoId=19282020" target="_blank">
                                        № 32615614489
                                    </a>
</div>
<div class="registry-entry__header-mid__title text-normal">
                                    
                                        
                                            Закупка завершена
                                        
                                        
                                    
                                </div>
</div>
</div>
<div class="registry-entry__body">
<div class="registry-entry__body-block">
<div class="registry-entry__body-title">Объект закупки</div>
<div class="registry-entry__body-value">Поставка <span class="highlightColor">ноутбуков</span></div>
</div>
<div class="registry-entry__body-block">
<div class="registry-entry__body-title">Заказчик</div>
<div class="registry-entry__body-href">
<a href="/epz/organization/view223/info.html?agencyId=481440" target="_blank">
                                            ГОСУДАРСТВЕННОЕ АВТОНОМНОЕ УЧРЕЖДЕНИЕ КАЛИНИНГРАДСКОЙ ОБЛАСТИ "СТАДИОН "КАЛИНИНГРАД"
                                        </a>
</div>
</div>
</div>
</div>
<div class="col col d-flex flex-column registry-entry__right-block b-left">
<div class="price-block">
<div class="price-block__title">Начальная цена
                            
                            </div>
<div class="price-block__value" style="overflow-wrap:anywhere">
                                313 769,00 ₽
                            </div>
</div>
<div class="data-block mt-auto">
<div class="row">
<div class="col-6">
<div class="data-block__title">Размещено</div>
<div class="data-block__value">16.01.2026</div>
</div>
<div class="col-6">
<div class="data-block__title">Обновлено</div>
<div class="data-block__value">16.01.2026</div>
</div>
</div>
</div>
<div class="href-block mt-auto d-none">
<div class="href d-flex">
<a href="/epz/order/notice/notice223/documents.html?noticeInfoId=19282020" target="_blank">
                                        Документы
                                    </a>
</div>
<div class="href d-flex">
<a href="/epz/order/notice/notice223/contract-info.html?noticeInfoId=19282020" target="_blank">
                                        Договор
                                    </a>
</div>
<div class="href align-self-center">
<a class="cursorPointer" onclick="openPlanGraphSearchUrl('32615614489')">
                                        План закупки
                                    </a>
</div>
<div class="href d-flex">
<a onclick="openComplaintSearch('32615614489', false, true, false)">
                                        Жалоба
                                    </a>
</div>
</div>
</div>
</div>
</div>
```

### Файл: `test_direct_response.html`
```html

















    
        
        
        
        
        
        
        
        
        
    





<!DOCTYPE html>
<html>







<head>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
    <meta name="description" content="Официальный сайт единой информационной системы в сфере закупок 44 ФЗ и 223 ФЗ"/>
    <meta name="apple-itunes-app" content="app-id=1457694118">
    <meta name="google-play-app" content="app-id=ru.gov.zakupki.mobile">

    <title>Закупки</title>
    <script type="text/javascript">
        var contextPath = "/epz/order";
        var epzMainPublicUrl = "/epz/main/public/";
        var serverHost = '/';
    </script>

    <script type="text/javascript" src="/static/useractivityrecordplugin/js/recordSupportSystem.js"></script>

    <link href="/epz/static/images/icons/Portal.ico" rel="shortcut icon">

    
        
        
            <link type="text/css" rel="stylesheet" media="all" href="/epz/static/css/app.css"/>
        
    

    <link type="text/css" rel="stylesheet" media="all" href="/epz/static/css/skin.css"/>
    <link type="text/css" rel="stylesheet" href="/epz/static/css/jquery.datepick.css"/>

    <link type="text/css" rel="stylesheet" href="/epz/static/css/ui.dynatree.css"/>
    
        
        
            <link type="text/css" rel="stylesheet" href="/epz/static/css/jquery_msgbox.css"/>
        
    
    
    
    <script src="/epz/static/js/d3.v5.min.js"></script>
    <script src="/epz/static/js/jquery-3.3.1.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/ui_autocomplete.js"></script>
    <script type="text/javascript" src="/epz/static/js/jquery-migrate-3.0.1.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/validation/jquery.validate.js"></script>
    <script type="text/javascript" src="/epz/static/js/mustache.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/jquery.price_format.1.7.js"></script>
    <script type="text/javascript" src="/epz/static/js/jquery.jcarousel.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/jquery.maskedinput.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/jquery.cookie.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/js.cookie.js"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            var notUsual = (($.cookie("usePoorVisionOption") == 'true') && $(".goodVisionLink").length == 0);
            var notPoorVision = (($.cookie("usePoorVisionOption") != 'true') && $(".poorVisionLink").length == 0);
            if (notUsual || notPoorVision){
                location.reload();
            }
        });
        
        $(window).ready(function() {
            $('body').animate({opacity:'1'},300);
        });
    </script>
    <script type="text/javascript" src="/epz/static/js/jquery.dynatree.js"></script>
    <script type="text/javascript" src="/epz/static/js/jquery.ui.datepicker-ru.js"></script>
    <script type="text/javascript" src="/epz/static/js/moment.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/moment-timezone.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/validation/jquery.numeric.js"></script>
    
    <script type="text/javascript" src="/epz/static/js/action-switch.js"></script>
    <script type="text/javascript" src="/epz/static/js/browser.js"></script>
    
        
        
            <script type="text/javascript" src="/epz/static/js/app.js"></script>
        
    
    <script type="text/javascript" src="/epz/static/js/common/hints.js"></script>
    <script type="text/javascript" src="/epz/static/js/baseLayout.js"></script>
    <script type="text/javascript" src="/epz/static/js/script.js"></script>
    <script type="text/javascript" src="/epz/static/js/checkNotice.js"></script>
    <script type="text/javascript" src="/epz/static/js/common/config.js"></script>
    <script type="text/javascript" src="/epz/static/js/common/choose-headagency.js"></script>
    <script type="text/javascript" src="/epz/static/js/common/choose-okpd.js"></script>
    <script type="text/javascript" src="/epz/static/js/custom.js"></script>
    <script type="text/javascript" src="/epz/static/js/popupCommon.js"></script>
    <script type="text/javascript" src="/epz/static/js/common/choose-organization.js"></script>
    <script type="text/javascript" src="/epz/static/js/URI.js"></script>
    <script type="text/javascript" src="/epz/static/js/common/analytics.js"></script>
    <script type="text/javascript" src="/epz/static/js/jquery_msgBox.js"></script>
    <script type="text/javascript" src="/epz/static/js/keyboardControl.js"></script>
    <script type="text/javascript" src="/epz/static/js/customScrollbar.js"></script>
    <script type="text/javascript" src="/epz/static/js/common/ssl-checker.js"></script>
    
        
        
            <script type="text/javascript" src="/epz/static/js/keyboardNavigationRules.js"></script>
        
    
    <script type="text/javascript">if (!window.console) console = {
        log: function () {
        }
    };</script>

    



<script type="text/javascript">
    epzCommonConfig.initCommonConfig({
        contextPath: '/epz/order',
        smartSearchEnable: true,

        urls: {
            epzMainPublicUrl: '/epz/main/public/',
            epzNsiUrl: '/epz/nsi/',
            epzOrderUrl: '/epz/order/',
            epzOrderPlanUrl: '/epz/orderplan/',
            epzOrderClauseUrl: '/epz/orderclause/',
            epzContractUrl: '/epz/contract/',
            epzContractFz223Url: '/epz/contractfz223/',
            epzContractReportingUrl: '/epz/contractreporting/',
            epzCustomerReportsUrl: '/epz/customerreports/',
            epzOrganizationUrl: '/epz/organization/',
            epzDishonestSupplierUrl: '/epz/dishonestsupplier/',
            epzComplaintUrl: '/epz/complaint/',
            epzBankGuaranteeUrl: '/epz/bankguarantee/',
            epzInspectionPlanUrl: '/epz/inspectionplan/',
            epzUnscheduledInspectionUrl: '/epz/unscheduledinspection/',
            epzControlResultUrl: '/epz/controlresult/',
            epzDizkUrl: '/epz/dizk/',
            epzEsUrl: '/analytics/hit/',
            epzFarmUrl: '/epz/farm/'
        }
    });
</script>
</head>
<body>

<script type="text/javascript">
    if ($.cookie('usePoorVisionOption') === 'true') {
        var body = $('body');
        var style = '', styleColor = '';
        var color = $.cookie('colorSpectrumForPoorVision');
        body.addClass('poorVision');
        if (color) {
            body.addClass(color + 'ColorSpectrum');
            switch (color) {
                case 'white':
                    style = '#ffffff';
                    styleColor = '#000000';
                    break;
                case 'black':
                    style = '#000000';
                    styleColor = '#ffffff'
                    break;
                case 'blue':
                    style = '#9DD1FF';
                    styleColor = '#063462';
                    break;
                case 'brown':
                    style = '#442713';
                    styleColor = '#a9e44d';
                    break;
                case 'biege':
                    style = '#F7F3D6';
                    styleColor = '#49442e';
                    break;
                default:
                    break;
            }
            body.css({backgroundColor: style, color:styleColor});
        }else{
            body.addClass('whiteColorSpectrum');
        }

        var fontSize = $.cookie('fontSizeForPoorVision');
        if (fontSize) {
            body.addClass('fontSizeForPoorVision' + fontSize);
        }else{
            body.addClass('fontSizeForPoorVision100');
        }
    }
</script>


    

    
    

















    
        
        
        
        
        
        
        
        
        
    











<style>
    .header-logo {
        top: -5px;
        background: none;
    }
</style>

<div id="critical_notice"></div>

    
    
        <header class="header header-top">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-5" style="z-index: 1;">
                        <span class="logo text-base-micro">Официальный сайт Единой информационной системы в сфере закупок</span>
                    </div>
                    <div class="col-1"></div>
                    <div class="col-3">
                        <a data-modalup href="/epz/nsi/kladr/chooseRegion.html">
                            <div class="region d-flex align-items-center pr-0" data-toggle="modal-region"
                                 data-target=".modal-region">
                      <span class="region-city w-space-nowrap">
                        <span class="region-city__icon">
                          <img src="/epz/static/img/icons/icon_region.svg"
                               title="Информация о местоположении пользователя используется в поисковых запросах для динамической детализации результатов поиска.">
                        </span>
                        <span class="region-city__text region-city__text_base text-base-micro">Мой регион: </span>
                      </span>
                                <span id = "chooseRegion">
                                <span class="region-city pl-1">
                        <span class="region-city__text region-city__text_prime text-base-micro region_name"
                              id="popUpUserRegion">
             
```

### Файл: `test_frontend.html`
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Тест НМЦК система</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .section { margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        .success { color: green; }
        .error { color: red; }
        .loading { color: blue; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        pre { background: #f5f5f5; padding: 10px; border-radius: 4px; overflow: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Тестирование НМЦК системы</h1>
        
        <div class="section">
            <h2>1. Создание сессии</h2>
            <button onclick="createSession()">Создать сессию</button>
            <div id="sessionResult"></div>
        </div>
        
        <div class="section">
            <h2>2. Загрузка истории задач</h2>
            <button onclick="loadTaskHistory()">Загрузить историю</button>
            <div id="historyResult"></div>
        </div>
        
        <div class="section">
            <h2>3. Создание задачи поиска</h2>
            <p>КТРУ: 17.12.14.110-00000019</p>
            <p>Наименование: Бумага для офисной техники</p>
            <p>Максимум результатов: 50</p>
            <button onclick="createSearchTask()">Создать задачу поиска</button>
            <div id="taskResult"></div>
        </div>
        
        <div class="section">
            <h2>4. Проверка результатов</h2>
            <button onclick="checkTaskResults()">Проверить результаты</button>
            <div id="resultsResult"></div>
        </div>
    </div>
    
    <script>
        const API_BASE = 'http://localhost:8000/api';
        
        async function createSession() {
            const resultDiv = document.getElementById('sessionResult');
            resultDiv.innerHTML = '<span class="loading">Создание сессии...</span>';
            
            try {
                const response = await fetch(`${API_BASE}/session`, {
                    credentials: 'include'
                });
                const data = await response.json();
                resultDiv.innerHTML = `<span class="success">Сессия создана: ${data.id}</span>`;
            } catch (error) {
                resultDiv.innerHTML = `<span class="error">Ошибка: ${error.message}</span>`;
            }
        }
        
        async function loadTaskHistory() {
            const resultDiv = document.getElementById('historyResult');
            resultDiv.innerHTML = '<span class="loading">Загрузка истории...</span>';
            
            try {
                const response = await fetch(`${API_BASE}/tasks?page=1&page_size=50`, {
                    credentials: 'include'
                });
                const data = await response.json();
                resultDiv.innerHTML = `
                    <span class="success">История загружена успешно</span>
                    <pre>${JSON.stringify(data, null, 2)}</pre>
                `;
            } catch (error) {
                resultDiv.innerHTML = `<span class="error">Ошибка загрузки истории: ${error.message}</span>`;
            }
        }
        
        async function createSearchTask() {
            const resultDiv = document.getElementById('taskResult');
            resultDiv.innerHTML = '<span class="loading">Создание задачи...</span>';
            
            try {
                const response = await fetch(`${API_BASE}/tasks/direct`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include',
                    body: JSON.stringify({
                        ktru_code: "17.12.14.110-00000019",
                        product_name: "Бумага для офисной техники",
                        vendor: null,
                        region: "Северо-Западный ФО",
                        period_years: 3,
                        max_results: 50,
                        characteristics: []
                    })
                });
                const data = await response.json();
                resultDiv.innerHTML = `
                    <span class="success">Задача создана: ${data.id}</span>
                    <pre>${JSON.stringify(data, null, 2)}</pre>
                `;
            } catch (error) {
                resultDiv.innerHTML = `<span class="error">Ошибка создания задачи: ${error.message}</span>`;
            }
        }
        
        async function checkTaskResults() {
            const resultDiv = document.getElementById('resultsResult');
            resultDiv.innerHTML = '<span class="loading">Проверка результатов...</span>';
            
            try {
                // Сначала получим историю, чтобы найти последнюю задачу
                const historyResponse = await fetch(`${API_BASE}/tasks?page=1&page_size=50`, {
                    credentials: 'include'
                });
                const historyData = await historyResponse.json();
                
                if (historyData.items.length === 0) {
                    resultDiv.innerHTML = '<span class="error">Нет задач для проверки</span>';
                    return;
                }
                
                const latestTask = historyData.items[0];
                const taskId = latestTask.id;
                
                // Проверим статус задачи
                const taskResponse = await fetch(`${API_BASE}/tasks/${taskId}`, {
                    credentials: 'include'
                });
                const taskData = await taskResponse.json();
                
                resultDiv.innerHTML = `
                    <span class="success">Статус задачи: ${taskData.status}</span>
                    <pre>${JSON.stringify(taskData, null, 2)}</pre>
                `;
                
                // Если задача завершена, покажем результаты
                if (taskData.status === 'done') {
                    const resultsResponse = await fetch(`${API_BASE}/tasks/${taskId}/result`, {
                        credentials: 'include'
                    });
                    const resultsData = await resultsResponse.json();
                    
                    resultDiv.innerHTML += `
                        <h3>Результаты поиска:</h3>
                        <pre>${JSON.stringify(resultsData.summary, null, 2)}</pre>
                        <h3>Контракты (${resultsData.contracts.length}):</h3>
                        <pre>${JSON.stringify(resultsData.contracts.slice(0, 3), null, 2)}</pre>
                    `;
                }
            } catch (error) {
                resultDiv.innerHTML = `<span class="error">Ошибка проверки результатов: ${error.message}</span>`;
            }
        }
    </script>
</body>
</html>
```

### Файл: `test_interface.html`
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Тест интерфейса НМЦК</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }
        .section {
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        .success {
            color: #4CAF50;
            font-weight: bold;
        }
        .error {
            color: #f44336;
            font-weight: bold;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px;
        }
        .button:hover {
            background-color: #45a049;
        }
        .status {
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 12px;
        }
        .status-done {
            background-color: #4CAF50;
            color: white;
        }
        .status-searching {
            background-color: #ff9800;
            color: white;
        }
        .status-queued {
            background-color: #2196F3;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Тест интерфейса системы НМЦК</h1>
        
        <div class="section">
            <h2>Статус системы</h2>
            <p id="system-status">Проверка...</p>
        </div>
        
        <div class="section">
            <h2>История поиска</h2>
            <div id="task-history">Загрузка...</div>
        </div>
        
        <div class="section">
            <h2>Результаты поиска (КТРУ: 17.12.14.110-00000019)</h2>
            <div id="search-results">Загрузка...</div>
        </div>
        
        <div class="section">
            <h2>Проверка пагинации</h2>
            <div id="pagination-test">Загрузка...</div>
        </div>
    </div>

    <script>
        const API_BASE = 'http://localhost:8000/api';
        
        async function checkSystemStatus() {
            try {
                const response = await fetch(`${API_BASE}/tasks?page=1&page_size=1`, {
                    credentials: 'include'
                });
                if (response.status === 401 || response.status === 200) {
                    document.getElementById('system-status').innerHTML = 
                        '<span class="success">✓ API доступен (требуется сессия)</span>';
                } else {
                    document.getElementById('system-status').innerHTML = 
                        '<span class="error">✗ Ошибка системы: ' + response.status + '</span>';
                }
            } catch (error) {
                document.getElementById('system-status').innerHTML = 
                    `<span class="error">✗ Ошибка подключения: ${error.message}</span>`;
            }
        }
        
        async function loadTaskHistory() {
            try {
                const response = await fetch(`${API_BASE}/tasks?page=1&page_size=50`, {
                    credentials: 'include'
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                
                let html = `<p>Всего задач: ${data.total}</p>`;
                
                if (data.items && data.items.length > 0) {
                    html += '<table>';
                    html += '<tr><th>ID</th><th>Дата</th><th>Статус</th><th>КТРУ</th><th>Наименование</th><th>Результат</th></tr>';
                    
                    data.items.forEach(task => {
                        const statusClass = `status status-${task.status}`;
                        html += `
                            <tr>
                                <td>${task.id ? task.id.substring(0, 8) + '...' : '-'}</td>
                                <td>${task.created_at ? new Date(task.created_at).toLocaleString() : '-'}</td>
                                <td><span class="${statusClass}">${task.status || '-'}</span></td>
                                <td>${task.ktru_code || '-'}</td>
                                <td>${task.product_name || '-'}</td>
                                <td>${task.summary || '-'}</td>
                            </tr>
                        `;
                    });
                    
                    html += '</table>';
                } else {
                    html += '<p>История поиска пуста</p>';
                }
                
                document.getElementById('task-history').innerHTML = html;
            } catch (error) {
                document.getElementById('task-history').innerHTML = 
                    `<span class="error">Ошибка загрузки истории: ${error.message}</span>`;
            }
        }
        
        async function loadSearchResults() {
            try {
                // Ищем задачу с КТРУ 17.12.14.110-00000019
                const response = await fetch(`${API_BASE}/tasks?page=1&page_size=50`, {
                    credentials: 'include'
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                
                const targetTask = data.items && data.items.find(task => 
                    task.ktru_code === '17.12.14.110-00000019' && 
                    task.product_name === 'Бумага для офисной техники'
                );
                
                if (targetTask) {
                    let html = `<p>Задача найдена: ${targetTask.id ? targetTask.id.substring(0, 8) + '...' : '-'}</p>`;
                    html += `<p>Статус: <span class="status status-${targetTask.status}">${targetTask.status || '-'}</span></p>`;
                    html += `<p>Результат: ${targetTask.summary || 'Нет данных'}</p>`;
                    
                    // Загружаем контракты
                    const contractsResponse = await fetch(`${API_BASE}/tasks/${targetTask.id}/contracts?page=1&page_size=10`, {
                        credentials: 'include'
                    });
                    
                    if (!contractsResponse.ok) {
                        throw new Error(`HTTP ${contractsResponse.status}: ${contractsResponse.statusText}`);
                    }
                    
                    const contractsData = await contractsResponse.json();
                    
                    html += `<p>Найдено контрактов: ${contractsData.total || 0}</p>`;
                    
                    if (contractsData.items && contractsData.items.length > 0) {
                        html += '<table>';
                        html += '<tr><th>№</th><th>Рег. номер</th><th>Поставщик</th><th>Цена</th><th>Совпадение</th><th>Тип</th></tr>';
                        
                        contractsData.items.forEach((contract, index) => {
                            html += `
                                <tr>
                                    <td>${index + 1}</td>
                                    <td>${contract.reg_number || '-'}</td>
                                    <td>${contract.supplier_name || '-'}</td>
                                    <td>${contract.unit_price ? Math.round(contract.unit_price) + ' руб.' : '-'}</td>
                                    <td>${contract.match_percent || '-'}%</td>
                                    <td>${contract.match_type || '-'}</td>
                                </tr>
                            `;
                        });
                        
                        html += '</table>';
                        
                        // Проверяем пагинацию
                        html += `<p>Пагинация: Страница ${contractsData.page || 1} из ${contractsData.total_pages || 1}`;
                        html += ` | Всего записей: ${contractsData.total || 0}`;
                        html += ` | Размер страницы: ${contractsData.page_size || 10}`;
                        html += ` | Следующая страница: ${contractsData.has_next ? 'Да' : 'Нет'}`;
                        html += ` | Предыдущая страница: ${contractsData.has_previous ? 'Да' : 'Нет'}</p>`;
                    }
                    
                    document.getElementById('search-results').innerHTML = html;
                } else {
                    document.getElementById('search-results').innerHTML = 
                        '<p class="error">Задача с указанными параметрами не найдена</p>';
                }
            } catch (error) {
                document.getElementById('search-results').innerHTML = 
                    `<span class="error">Ошибка загрузки результатов: ${error.message}</span>`;
            }
        }
        
        async function testPagination() {
            try {
                // Сначала получим список задач
                const tasksResponse = await fetch(`${API_BASE}/tasks?page=1&page_size=10`, {
                    credentials: 'include'
                });
                
                if (!tasksResponse.ok) {
                    throw new Error(`HTTP ${tasksResponse.status}: ${tasksResponse.statusText}`);
                }
                
                const tasksData = await tasksResponse.json();
                
                if (!tasksData.items || tasksData.items.length === 0) {
                    document.getElementById('pagination-test').innerHTML = 
                        '<p class="error">Нет задач для тестирования пагинации</p>';
                    return;
                }
                
                const taskId = tasksData.items[0].id;
                
                // Тестируем пагинацию с разными размерами страниц
                let html = '<h3>Тест пагинации</h3>';
                
                // Тест 1: 2 контракта на странице
                const response1 = await fetch(`${API_BASE}/tasks/${taskId}/contracts?page=1&page_size=2`, {
                    credentials: 'include'
                });
                
                if (!response1.ok) {
                    throw new Error(`HTTP ${response1.status}: ${response1.statusText}`);
                }
                
                const data1 = await response1.json();
                
                html += '<h4>Тест 1: 2 контракта на странице</h4>';
                html += `<p>Всего контрактов: ${data1.total || 0}</p>`;
                html += `<p>Страниц: ${data1.total_pages || 1}</p>`;
                html += `<p>Текущая страница: ${data1.page || 1}</p>`;
                html += `<p>Контрактов на странице: ${data1.items ? data1.items.length : 0}</p>`;
                html += `<p>Есть следующая страница: ${data1.has_next ? 'Да' : 'Нет'}</p>`;
                html += `<p>Есть предыдущая страница: ${data1.has_previous ? 'Да' : 'Нет'}</p>`;
                
                if (data1.items && data1.items.length > 0) {
                    html += '<table>';
                    html += '<tr><th>Рег. номер</th><th>Поставщик</th><th>Цена</th><th>Совпадение</th></tr>';
                    
                    data1.items.forEach(contract => {
                        html += `
                            <tr>
                                <td>${contract.reg_number || '-'}</td>
                                <td>${contract.supplier_name || '-'}</td>
                                <td>${contract.unit_price ? Math.round(contract.unit_price) + ' руб.' : '-'}</td>
                                <td>${contract.match_percent || '-'}%</td>
                            </tr>
                        `;
                    });
                    
                    html += '</table>';
                }
                
                // Тест 2: 3 контракта на странице
                const response2 = await fetch(`${API_BASE}/tasks/${taskId}/contracts?page=1&page_size=3`, {
                    credentials: 'include'
                });
                
                if (!response2.ok) {
                    throw new Error(`HTTP ${response2.status}: ${response2.statusText}`);
                }
                
                const data2 = await response2.json();
                
                html += '<h4>Тест 2: 3 контракта на странице</h4>';
                html += `<p>Всего контрактов: ${data2.total || 0}</p>`;
                html += `<p>Страниц: ${data2.total_pages || 1}</p>`;
                html += `<p>Текущая страница: ${data2.page || 1}</p>`;
                html += `<p>Контрактов на странице: ${data2.items ? data2.items.length : 0}</p>`;
                html += `<p>Есть следующая страница: ${data2.has_next ? 'Да' : 'Нет'}</p>`;
                html += `<p>Есть предыдущая страница: ${data2.has_previous ? 'Да' : 'Нет'}</p>`;
                
                document.getElementById('pagination-test').innerHTML = html;
            } catch (error) {
                document.getElementById('pagination-test').innerHTML = 
                    `<span class="error">Ошибка тестирования пагинации: ${error.message}</span>`;
            }
        }
        
        // Запускаем все проверки
        async function runAllTests() {
            await checkSystemStatus();
            await loadTaskHistory();
            await loadSearchResults();
            await testPagination();
        }
        
        // Запускаем при загрузке страницы
        document.addEventListener('DOMContentLoaded', runAllTests);
    </script>
</body>
</html>
```

### Файл: `test_response.html`
```html

















    
        
        
        
        
        
        
        
        
        
    





<!DOCTYPE html>
<html>







<head>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
    <meta name="description" content="Официальный сайт единой информационной системы в сфере закупок 44 ФЗ и 223 ФЗ"/>
    <meta name="apple-itunes-app" content="app-id=1457694118">
    <meta name="google-play-app" content="app-id=ru.gov.zakupki.mobile">

    <title>Закупки</title>
    <script type="text/javascript">
        var contextPath = "/epz/order";
        var epzMainPublicUrl = "/epz/main/public/";
        var serverHost = '/';
    </script>

    <script type="text/javascript" src="/static/useractivityrecordplugin/js/recordSupportSystem.js"></script>

    <link href="/epz/static/images/icons/Portal.ico" rel="shortcut icon">

    
        
        
            <link type="text/css" rel="stylesheet" media="all" href="/epz/static/css/app.css"/>
        
    

    <link type="text/css" rel="stylesheet" media="all" href="/epz/static/css/skin.css"/>
    <link type="text/css" rel="stylesheet" href="/epz/static/css/jquery.datepick.css"/>

    <link type="text/css" rel="stylesheet" href="/epz/static/css/ui.dynatree.css"/>
    
        
        
            <link type="text/css" rel="stylesheet" href="/epz/static/css/jquery_msgbox.css"/>
        
    
    
    
    <script src="/epz/static/js/d3.v5.min.js"></script>
    <script src="/epz/static/js/jquery-3.3.1.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/ui_autocomplete.js"></script>
    <script type="text/javascript" src="/epz/static/js/jquery-migrate-3.0.1.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/validation/jquery.validate.js"></script>
    <script type="text/javascript" src="/epz/static/js/mustache.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/jquery.price_format.1.7.js"></script>
    <script type="text/javascript" src="/epz/static/js/jquery.jcarousel.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/jquery.maskedinput.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/jquery.cookie.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/js.cookie.js"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            var notUsual = (($.cookie("usePoorVisionOption") == 'true') && $(".goodVisionLink").length == 0);
            var notPoorVision = (($.cookie("usePoorVisionOption") != 'true') && $(".poorVisionLink").length == 0);
            if (notUsual || notPoorVision){
                location.reload();
            }
        });
        
        $(window).ready(function() {
            $('body').animate({opacity:'1'},300);
        });
    </script>
    <script type="text/javascript" src="/epz/static/js/jquery.dynatree.js"></script>
    <script type="text/javascript" src="/epz/static/js/jquery.ui.datepicker-ru.js"></script>
    <script type="text/javascript" src="/epz/static/js/moment.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/moment-timezone.min.js"></script>
    <script type="text/javascript" src="/epz/static/js/validation/jquery.numeric.js"></script>
    
    <script type="text/javascript" src="/epz/static/js/action-switch.js"></script>
    <script type="text/javascript" src="/epz/static/js/browser.js"></script>
    
        
        
            <script type="text/javascript" src="/epz/static/js/app.js"></script>
        
    
    <script type="text/javascript" src="/epz/static/js/common/hints.js"></script>
    <script type="text/javascript" src="/epz/static/js/baseLayout.js"></script>
    <script type="text/javascript" src="/epz/static/js/script.js"></script>
    <script type="text/javascript" src="/epz/static/js/checkNotice.js"></script>
    <script type="text/javascript" src="/epz/static/js/common/config.js"></script>
    <script type="text/javascript" src="/epz/static/js/common/choose-headagency.js"></script>
    <script type="text/javascript" src="/epz/static/js/common/choose-okpd.js"></script>
    <script type="text/javascript" src="/epz/static/js/custom.js"></script>
    <script type="text/javascript" src="/epz/static/js/popupCommon.js"></script>
    <script type="text/javascript" src="/epz/static/js/common/choose-organization.js"></script>
    <script type="text/javascript" src="/epz/static/js/URI.js"></script>
    <script type="text/javascript" src="/epz/static/js/common/analytics.js"></script>
    <script type="text/javascript" src="/epz/static/js/jquery_msgBox.js"></script>
    <script type="text/javascript" src="/epz/static/js/keyboardControl.js"></script>
    <script type="text/javascript" src="/epz/static/js/customScrollbar.js"><
```

