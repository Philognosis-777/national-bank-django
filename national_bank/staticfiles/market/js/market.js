// Market Page JavaScript

// ===== GLOBAL VARIABLES =====
let currentLang = localStorage.getItem('nbe-language-preference') || 'en'; // Default language
let exchangeRateChart;
const exchangeRateData = {};
const historicalData = [];

// ===== LANGUAGE SWITCHER CLASS =====
class LanguageSwitcher {
    constructor() {
        this.currentLang = localStorage.getItem('nbe-language-preference') || 'en';
        this.langToggle = document.getElementById('langToggle');
        this.init();
    }
    
    init() {
        this.updateToggleButton();
        this.setupEventListeners();
        this.setupTooltip();
        this.applyInitialLanguage();
    }
    
    updateToggleButton() {
        const text = this.currentLang === 'en' ? 'አማርኛ' : 'English';
        
        if (this.langToggle) {
            const langText = this.langToggle.querySelector('.lang-text');
            if (langText) {
                langText.textContent = text;
            }
        }
    }
    
    setupEventListeners() {
        if (this.langToggle) {
            this.langToggle.addEventListener('click', (e) => this.handleToggleClick(e));
        }
        
        // Listen for language changes from other components
        document.addEventListener('languageChanged', (e) => {
            this.currentLang = e.detail.lang;
            this.updateToggleButton();
        });
    }
    
    handleToggleClick(event) {
        // Create ripple effect
        this.createRippleEffect(event, this.langToggle);
        
        // Toggle language
        this.currentLang = this.currentLang === 'en' ? 'am' : 'en';
        
        // Update button text
        this.updateToggleButton();
        
        // Switch language globally
        this.switchLanguage(this.currentLang);
        
        // Update document language
        document.documentElement.lang = this.currentLang;
        
        // Save preference
        localStorage.setItem('nbe-language-preference', this.currentLang);
        
        // Trigger custom event
        const languageEvent = new CustomEvent('languageChanged', { 
            detail: { lang: this.currentLang }
        });
        document.dispatchEvent(languageEvent);
    }
    
    switchLanguage(lang) {
        // Update all elements with English and Amharic classes
        this.updateLanguageClasses(lang);
        
        // Update elements with data attributes
        this.updateDataAttributes(lang);
        
        // Update font families
        this.updateFontFamily(lang);
        
        // Update any chart labels if chart exists
        this.updateChartLabels(lang);
    }
    
    updateLanguageClasses(lang) {
        // Show/hide English and Amharic elements
        document.querySelectorAll('.english').forEach(el => {
            el.style.display = lang === 'en' ? 'inline' : 'none';
        });
        
        document.querySelectorAll('.amharic').forEach(el => {
            el.style.display = lang === 'am' ? 'inline' : 'none';
        });
        
        // Special handling for header titles
        document.querySelectorAll('.brand-text h1, .tagline').forEach(el => {
            if (el.classList.contains('english')) {
                el.style.display = lang === 'en' ? 'block' : 'none';
            }
            if (el.classList.contains('amharic')) {
                el.style.display = lang === 'am' ? 'block' : 'none';
            }
        });
    }
    
    updateDataAttributes(lang) {
        document.querySelectorAll('[data-en], [data-am]').forEach(element => {
            if (lang === 'en' && element.hasAttribute('data-en')) {
                element.textContent = element.getAttribute('data-en');
            } else if (lang === 'am' && element.hasAttribute('data-am')) {
                element.textContent = element.getAttribute('data-am');
            }
        });
    }
    
    updateFontFamily(lang) {
        const footer = document.querySelector('.main-footer');
        if (footer) {
            footer.style.fontFamily = lang === 'am' 
                ? "'Noto Sans Ethiopic', 'Roboto', sans-serif" 
                : "'Roboto', 'Noto Sans Ethiopic', sans-serif";
        }
        
        document.body.style.fontFamily = lang === 'am'
            ? "'Noto Sans Ethiopic', 'Roboto', sans-serif"
            : "'Roboto', 'Noto Sans Ethiopic', sans-serif";
    }
    
    updateChartLabels(lang) {
        if (exchangeRateChart) {
            // Update chart title and axis labels if needed
            const yAxis = exchangeRateChart.options.scales.y;
            if (yAxis && yAxis.title) {
                yAxis.title.text = lang === 'en' 
                    ? 'Exchange Rate (ETB)' 
                    : 'የምንዛሪ ተመን (ETB)';
            }
            exchangeRateChart.update();
        }
    }
    
    createRippleEffect(event, button) {
        if (!button) return;
        
        const circle = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        circle.classList.add('ripple');
        circle.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
            width: ${size}px;
            height: ${size}px;
            top: ${y}px;
            left: ${x}px;
            pointer-events: none;
            z-index: 1000;
        `;
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(circle);
        
        setTimeout(() => circle.remove(), 600);
    }
    
    setupTooltip() {
        const languageToggle = document.querySelector('.language-toggle');
        if (languageToggle) {
            languageToggle.setAttribute('data-tooltip', 'Switch Language / ቋንቋ ቀይር');
        }
    }
    
    applyInitialLanguage() {
        if (this.currentLang === 'am') {
            this.switchLanguage('am');
            document.documentElement.lang = 'am';
        }
    }
    
    getCurrentLanguage() {
        return this.currentLang;
    }
}

// ===== ADVANCED HEADER CLASS =====
class AdvancedHeader {
    constructor() {
        this.header = document.querySelector('.main-header');
        this.navLinks = document.querySelectorAll('.nav-link');
        this.init();
    }
    
    init() {
        this.handleScroll();
        this.addHoverEffects();
        this.addActiveClass();
        this.setupMobileMenu();
        
        // Add scroll event listener
        window.addEventListener('scroll', () => this.handleScroll());
    }
    
    handleScroll() {
        if (!this.header) return;
        
        if (window.scrollY > 50) {
            this.header.classList.add('scrolled');
        } else {
            this.header.classList.remove('scrolled');
        }
    }
    
    addHoverEffects() {
        this.navLinks.forEach(link => {
            const icon = link.querySelector('i');
            
            link.addEventListener('mouseenter', () => {
                if (icon) {
                    icon.style.transform = 'translateY(-5px)';
                }
            });
            
            link.addEventListener('mouseleave', () => {
                if (icon) {
                    icon.style.transform = 'translateY(0)';
                }
            });
        });
    }
    
    addActiveClass() {
        const currentPath = window.location.pathname;
        
        this.navLinks.forEach(link => {
            const linkPath = link.getAttribute('href');
            
            if (currentPath.includes(linkPath) && linkPath !== 'index.html') {
                link.classList.add('active');
            } else if (currentPath.endsWith('/') && linkPath === 'index.html') {
                link.classList.add('active');
            } else if (currentPath.includes('market') && linkPath.includes('market')) {
                link.classList.add('active');
            }
            
            // Update active link on click
            link.addEventListener('click', (e) => {
                // Don't prevent default - allow navigation
                this.navLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            });
        });
    }
    
    setupMobileMenu() {
        const toggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('#navbarNav');
        
        if (toggler && navbarCollapse) {
            toggler.addEventListener('click', () => {
                navbarCollapse.classList.toggle('show');
                
                // Animate hamburger icon
                const icon = toggler.querySelector('.navbar-toggler-icon');
                if (icon) {
                    icon.style.transform = navbarCollapse.classList.contains('show') 
                        ? 'rotate(90deg)' 
                        : 'rotate(0)';
                }
            });
            
            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!navbarCollapse.contains(e.target) && 
                    !toggler.contains(e.target) && 
                    navbarCollapse.classList.contains('show')) {
                    navbarCollapse.classList.remove('show');
                    const icon = toggler.querySelector('.navbar-toggler-icon');
                    if (icon) {
                        icon.style.transform = 'rotate(0)';
                    }
                }
            });
        }
    }
}

// ===== MARKET DATA FUNCTIONS =====

// Generate random history data
function generateHistoryData(baseRate, volatility) {
    const history = [];
    const today = new Date();
    
    for (let i = 90; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(today.getDate() - i);
        
        // Generate random rate with some volatility
        const randomFactor = 1 + (Math.random() - 0.5) * volatility / 100;
        const rate = baseRate * randomFactor;
        
        history.push({
            date: date.toISOString().split('T')[0],
            rate: parseFloat(rate.toFixed(2))
        });
    }
    
    return history;
}

// Generate historical table data
function generateHistoricalData() {
    const data = [];
    const today = new Date();
    
    for (let i = 0; i < 10; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() - i * 3);
        
        const dateStr = date.toISOString().split('T')[0];
        
        data.push({
            date: dateStr,
            usd: (54.80 + (Math.random() - 0.5) * 2).toFixed(2),
            eur: (59.45 + (Math.random() - 0.5) * 2).toFixed(2),
            gbp: (67.32 + (Math.random() - 0.5) * 2).toFixed(2)
        });
    }
    
    return data;
}

// Initialize exchange rate data
function initializeExchangeRateData() {
    Object.assign(exchangeRateData, {
        usd: {
            code: 'USD',
            name: 'US Dollar',
            nameAm: 'የአሜሪካ ዶላር',
            rate: 54.80,
            change: 0.25,
            history: generateHistoryData(54.80, 0.5)
        },
        eur: {
            code: 'EUR',
            name: 'Euro',
            nameAm: 'ዩሮ',
            rate: 59.45,
            change: -0.12,
            history: generateHistoryData(59.45, 0.6)
        },
        gbp: {
            code: 'GBP',
            name: 'British Pound',
            nameAm: 'የብሪታንያ ፓውንድ',
            rate: 67.32,
            change: 0.18,
            history: generateHistoryData(67.32, 0.7)
        },
        cny: {
            code: 'CNY',
            name: 'Chinese Yuan',
            nameAm: 'ቻይንኛ ዩዋን',
            rate: 7.95,
            change: 0.05,
            history: generateHistoryData(7.95, 0.2)
        },
        jpy: {
            code: 'JPY',
            name: 'Japanese Yen',
            nameAm: 'ጃፓንኛ የን',
            rate: 0.41,
            change: -0.01,
            history: generateHistoryData(0.41, 0.05)
        },
        aed: {
            code: 'AED',
            name: 'UAE Dirham',
            nameAm: 'የዩኤኢ ዲርሃም',
            rate: 14.92,
            change: 0.15,
            history: generateHistoryData(14.92, 0.3)
        },
        sar: {
            code: 'SAR',
            name: 'Saudi Riyal',
            nameAm: 'የሳውዲ ሪያል',
            rate: 14.61,
            change: 0.12,
            history: generateHistoryData(14.61, 0.25)
        },
        kes: {
            code: 'KES',
            name: 'Kenyan Shilling',
            nameAm: 'ኬንያን ሺሊንግ',
            rate: 0.42,
            change: 0.02,
            history: generateHistoryData(0.42, 0.1)
        }
    });
}

// Get color for currency
function getCurrencyColor(currencyCode, opacity = 1) {
    const colors = {
        'USD': `rgba(0, 100, 0, ${opacity})`, // Green
        'EUR': `rgba(0, 0, 255, ${opacity})`, // Blue
        'GBP': `rgba(255, 0, 0, ${opacity})`, // Red
        'CNY': `rgba(255, 165, 0, ${opacity})`, // Orange
        'JPY': `rgba(128, 0, 128, ${opacity})`, // Purple
        'AED': `rgba(0, 128, 128, ${opacity})`, // Teal
        'SAR': `rgba(139, 69, 19, ${opacity})`, // Brown
        'KES': `rgba(255, 192, 203, ${opacity})` // Pink
    };
    
    return colors[currencyCode] || `rgba(128, 128, 128, ${opacity})`;
}

// Get chart data based on time range and currency selection
function getChartData(days, currency) {
    const labels = [];
    const datasets = [];
    
    // Generate labels for the selected time range
    const today = new Date();
    for (let i = days - 1; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(today.getDate() - i);
        
        // Format date based on time range
        let dateStr;
        if (days <= 30) {
            dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        } else if (days <= 90) {
            // Show week intervals
            dateStr = (i % 7 === 0 || i === days - 1) 
                ? date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
                : '';
        } else {
            // Show month intervals
            dateStr = (date.getDate() === 1 || i === days - 1)
                ? date.toLocaleDateString('en-US', { month: 'short' })
                : '';
        }
        
        labels.push(dateStr);
    }
    
    // Prepare datasets based on currency selection
    if (currency === 'all') {
        // Show all major currencies
        const majorCurrencies = ['usd', 'eur', 'gbp'];
        
        majorCurrencies.forEach(curr => {
            const currencyData = exchangeRateData[curr];
            if (currencyData) {
                const data = currencyData.history.slice(-days).map(item => item.rate);
                
                datasets.push({
                    label: currencyData.code,
                    data: data,
                    borderColor: getCurrencyColor(currencyData.code),
                    backgroundColor: getCurrencyColor(currencyData.code, 0.1),
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4
                });
            }
        });
    } else {
        // Show selected currency
        const currencyData = exchangeRateData[currency];
        if (currencyData) {
            const data = currencyData.history.slice(-days).map(item => item.rate);
            
            datasets.push({
                label: currencyData.code,
                data: data,
                borderColor: getCurrencyColor(currencyData.code),
                backgroundColor: getCurrencyColor(currencyData.code, 0.1),
                borderWidth: 3,
                fill: true,
                tension: 0.4
            });
        }
    }
    
    return {
        labels: labels,
        datasets: datasets
    };
}

// Initialize Chart.js
function initializeChart() {
    const canvas = document.getElementById('exchangeRateChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Get initial data
    const timeRangeSelect = document.getElementById('timeRange');
    const currencySelect = document.getElementById('currencySelect');
    
    if (!timeRangeSelect || !currencySelect) return;
    
    const timeRange = parseInt(timeRangeSelect.value);
    const currency = currencySelect.value;
    
    const chartData = getChartData(timeRange, currency);
    
    exchangeRateChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += context.parsed.y.toFixed(2) + ' ETB';
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: true
                    }
                },
                y: {
                    beginAtZero: false,
                    grid: {
                        display: true
                    },
                    title: {
                        display: true,
                        text: 'Exchange Rate (ETB)'
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'nearest'
            }
        }
    });
}

// Update chart
function updateChart() {
    if (!exchangeRateChart) return;
    
    const timeRangeSelect = document.getElementById('timeRange');
    const currencySelect = document.getElementById('currencySelect');
    
    if (!timeRangeSelect || !currencySelect) return;
    
    const timeRange = parseInt(timeRangeSelect.value);
    const currency = currencySelect.value;
    
    const newData = getChartData(timeRange, currency);
    
    exchangeRateChart.data.labels = newData.labels;
    exchangeRateChart.data.datasets = newData.datasets;
    exchangeRateChart.update();
}

// Populate currency table
function populateCurrencyTable() {
    const tableBody = document.getElementById('currencyTable');
    if (!tableBody) return;
    
    tableBody.innerHTML = '';
    
    Object.values(exchangeRateData).forEach(currency => {
        const row = document.createElement('tr');
        row.className = 'currency-row';
        
        const changeValue = currency.change;
        const changeClass = changeValue > 0 ? 'positive' : changeValue < 0 ? 'negative' : 'neutral';
        const changeIcon = changeValue > 0 ? 'fa-arrow-up' : changeValue < 0 ? 'fa-arrow-down' : 'fa-minus';
        const changeSign = changeValue > 0 ? '+' : '';
        
        row.innerHTML = `
            <td>
                <span class="english">${currency.name}</span>
                <span class="amharic" style="display: none;">${currency.nameAm}</span>
                <br>
                <small>${currency.code}</small>
            </td>
            <td>${currency.rate.toFixed(2)}</td>
            <td>
                <span class="change-indicator ${changeClass}">
                    <i class="fas ${changeIcon}"></i>
                    <span>${changeSign}${currency.change.toFixed(2)}%</span>
                </span>
            </td>
        `;
        
        tableBody.appendChild(row);
    });
    
    // Apply current language to the new rows
    const languageSwitcher = window.languageSwitcher;
    if (languageSwitcher) {
        languageSwitcher.updateLanguageClasses(languageSwitcher.currentLang);
    }
}

// Populate historical table
function populateHistoricalTable() {
    const tableBody = document.getElementById('historicalTable');
    if (!tableBody) return;
    
    tableBody.innerHTML = '';
    
    const historicalData = generateHistoricalData();
    
    historicalData.forEach(item => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${item.date}</td>
            <td>${item.usd}</td>
            <td>${item.eur}</td>
            <td>${item.gbp}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

// Update displayed rates
function updateDisplayedRates() {
    // Update the market cards
    const marketCards = document.querySelectorAll('.market-card');
    
    if (marketCards.length >= 4) {
        const usdRate = marketCards[1]?.querySelector('.currency-rate');
        const eurRate = marketCards[2]?.querySelector('.currency-rate');
        const gbpRate = marketCards[3]?.querySelector('.currency-rate');
        
        if (usdRate) usdRate.textContent = exchangeRateData.usd?.rate.toFixed(2) || '54.80';
        if (eurRate) eurRate.textContent = exchangeRateData.eur?.rate.toFixed(2) || '59.45';
        if (gbpRate) gbpRate.textContent = exchangeRateData.gbp?.rate.toFixed(2) || '67.32';
    }
    
    // Update change indicators
    updateChangeIndicator('usd', exchangeRateData.usd?.change || 0);
    updateChangeIndicator('eur', exchangeRateData.eur?.change || 0);
    updateChangeIndicator('gbp', exchangeRateData.gbp?.change || 0);
    
    // Update currency table
    populateCurrencyTable();
}

// Update change indicator
function updateChangeIndicator(currency, change) {
    const cardIndex = getCardIndex(currency);
    const card = document.querySelector(`.market-card:nth-child(${cardIndex})`);
    if (!card) return;
    
    const indicator = card.querySelector('.change-indicator');
    if (!indicator) return;
    
    const icon = indicator.querySelector('i');
    const text = indicator.querySelector('span:not(.fa)');
    
    if (!icon || !text) return;
    
    // Update classes
    indicator.className = 'change-indicator';
    
    if (change > 0) {
        indicator.classList.add('positive');
        icon.className = 'fas fa-arrow-up';
        text.textContent = `+${change.toFixed(2)}%`;
    } else if (change < 0) {
        indicator.classList.add('negative');
        icon.className = 'fas fa-arrow-down';
        text.textContent = `${change.toFixed(2)}%`;
    } else {
        indicator.classList.add('neutral');
        icon.className = 'fas fa-minus';
        text.textContent = '0.00%';
    }
}

// Helper function to get card index
function getCardIndex(currency) {
    const indices = {
        'usd': 2,
        'eur': 3,
        'gbp': 4
    };
    
    return indices[currency] || 2;
}

// ===== BACK TO TOP FUNCTIONALITY =====
function initBackToTop() {
    const backToTopButton = document.getElementById('backToTop');
    if (!backToTopButton) return;
    
    function toggleBackToTopButton() {
        if (window.pageYOffset > 300) {
            backToTopButton.classList.add('visible');
        } else {
            backToTopButton.classList.remove('visible');
        }
    }
    
    window.addEventListener('scroll', toggleBackToTopButton);
    
    backToTopButton.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Check initial scroll position
    toggleBackToTopButton();
}

// ===== LOGO LOADING FUNCTION =====
function loadLogoImage() {
    const logoImg = document.querySelector('.footer-logo .logo-img');
    if (logoImg) {
        // Check if image exists
        const img = new Image();
        img.src = logoImg.src;
        
        img.onload = function() {
            // Image loaded successfully
            logoImg.classList.add('loaded');
            console.log('Logo image loaded successfully');
        };
        
        img.onerror = function() {
            // Image failed to load - keep Font Awesome icon visible
            logoImg.style.display = 'none';
            console.warn('Logo image failed to load, using Font Awesome fallback');
        };
    }
}

// ===== FOOTER HOVER EFFECTS =====
function initFooterEffects() {
    // Add hover effects to footer boxes
    document.querySelectorAll('.footer-box').forEach(box => {
        box.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        box.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Add click effects to social links
    document.querySelectorAll('.social-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Show alert for demo purposes
            const platform = this.querySelector('span')?.textContent || 'social media';
            alert(`In a real implementation, this would navigate to the National Bank of Ethiopia ${platform} page.`);
        });
    });
    
    // Add click effect to footer links for demo
    document.querySelectorAll('.footer-links a, .footer-box ul li a').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const linkText = this.textContent || 'page';
            alert(`This would navigate to the ${linkText} page in a real implementation.`);
        });
    });
    
    // Add click effect to logo
    const footerLogo = document.querySelector('.footer-logo');
    if (footerLogo) {
        footerLogo.addEventListener('click', function(e) {
            e.preventDefault();
            alert('This would navigate to the National Bank of Ethiopia homepage in a real implementation.');
        });
        
        // Add title attribute for accessibility
        footerLogo.setAttribute('title', 'National Bank of Ethiopia - Home');
    }
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('Market page loaded');
    
    // Initialize data
    initializeExchangeRateData();
    
    // Initialize components
    const languageSwitcher = new LanguageSwitcher();
    window.languageSwitcher = languageSwitcher; // Make globally available
    
    const advancedHeader = new AdvancedHeader();
    
    // Initialize market components
    initializeChart();
    populateCurrencyTable();
    populateHistoricalTable();
    
    // Initialize UI components
    initBackToTop();
    loadLogoImage();
    initFooterEffects();
    
    // Set up event listeners for chart controls
    const timeRangeSelect = document.getElementById('timeRange');
    const currencySelect = document.getElementById('currencySelect');
    
    if (timeRangeSelect) {
        timeRangeSelect.addEventListener('change', updateChart);
    }
    
    if (currencySelect) {
        currencySelect.addEventListener('change', updateChart);
    }
    
    // Add fade-in animation delays
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Add click event to currency rows for detailed view
    document.addEventListener('click', function(e) {
        const row = e.target.closest('.currency-row');
        if (row) {
            const currencyName = row.querySelector('td')?.textContent.split('\n')[0].trim() || '';
            
            // Log for demo
            console.log(`Showing detailed view for ${currencyName}`);
            
            // Update chart to show this currency only
            const codeElement = row.querySelector('small');
            if (codeElement) {
                const currencyCode = codeElement.textContent.toLowerCase();
                if (exchangeRateData[currencyCode]) {
                    const currencySelect = document.getElementById('currencySelect');
                    if (currencySelect) {
                        currencySelect.value = currencyCode;
                        updateChart();
                        
                        // Scroll to chart
                        const chartContainer = document.querySelector('.chart-container');
                        if (chartContainer) {
                            chartContainer.scrollIntoView({
                                behavior: 'smooth'
                            });
                        }
                    }
                }
            }
        }
    });
    
    // Simulate real-time updates (every 30 seconds)
    setInterval(() => {
        // Update exchange rates with small random changes
        Object.keys(exchangeRateData).forEach(key => {
            const currency = exchangeRateData[key];
            
            // Small random change (-0.1% to +0.1%)
            const change = (Math.random() - 0.5) * 0.2;
            const newRate = currency.rate * (1 + change / 100);
            
            // Update rate and change
            currency.rate = parseFloat(newRate.toFixed(2));
            currency.change = parseFloat((currency.change + change).toFixed(2));
            
            // Add new data point to history
            const today = new Date().toISOString().split('T')[0];
            const lastDate = currency.history[currency.history.length - 1]?.date;
            
            if (today !== lastDate) {
                // Add new day
                currency.history.push({
                    date: today,
                    rate: currency.rate
                });
                
                // Keep only last 90 days
                if (currency.history.length > 90) {
                    currency.history.shift();
                }
            } else {
                // Update today's rate
                if (currency.history.length > 0) {
                    currency.history[currency.history.length - 1].rate = currency.rate;
                }
            }
        });
        
        // Update displayed values
        updateDisplayedRates();
        
        // Update chart if needed
        if (document.getElementById('currencySelect')?.value !== 'all') {
            updateChart();
        }
        
    }, 30000); // Update every 30 seconds
    
    // Add keyboard navigation support
    document.addEventListener('keydown', function(e) {
        // Space or Enter key on language button
        if ((e.key === 'Enter' || e.key === ' ') && 
            e.target.id === 'langToggle') {
            e.preventDefault();
            e.target.click();
        }
        
        // Escape key - close mobile menu if open
        if (e.key === 'Escape') {
            const navbarCollapse = document.querySelector('#navbarNav.show');
            const toggler = document.querySelector('.navbar-toggler');
            if (navbarCollapse && toggler) {
                navbarCollapse.classList.remove('show');
                const icon = toggler.querySelector('.navbar-toggler-icon');
                if (icon) {
                    icon.style.transform = 'rotate(0)';
                }
            }
        }
    });
});

// Export for use in other scripts if needed
window.NBEMarket = {
    LanguageSwitcher,
    AdvancedHeader,
    updateChart,
    populateCurrencyTable,
    getCurrentLanguage: () => window.languageSwitcher?.getCurrentLanguage() || 'en'
};