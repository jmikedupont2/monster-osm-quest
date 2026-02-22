const TENFOLD=["🌀 A","🔱 AIII","⚛️ AI","🌳 BDI","💎 D","🌊 DIII","🧬 AII","🔮 CII","⚡ C","🌌 CI"];
const EMOJIS=['🏙','🌊','🏔','🛣','🌳','🏛','🐯','⚡','🧬','🌙','📡','🎭','👁','🔬','🎓'];
const OSM_LOCATIONS={
    0:{name:"Pacific Ocean",emoji:"🌊",nodes:0},
    5:{name:"Himalayas",emoji:"🏔",nodes:225e9},
    10:{name:"Amazon",emoji:"🌳",nodes:45e10},
    17:{name:"Giza Pyramids",emoji:"🐯",nodes:765e9,special:"CUSP"},
    23:{name:"Silicon Valley",emoji:"🧬",nodes:1035e9,special:"CONSCIOUSNESS"},
    30:{name:"New York",emoji:"🏙",nodes:135e10},
    35:{name:"Tokyo",emoji:"🗼",nodes:1575e9},
    40:{name:"London",emoji:"🏰",nodes:18e11},
    59:{name:"Ramanujan Temple",emoji:"🌙",nodes:2655e9,special:"MEMORY"},
    70:{name:"Omega Point",emoji:"⚡",nodes:315e10}
};

class MonsterQuest {
    constructor() {
        this.playerX = 0;
        this.playerY = 0;
        this.viewWidth = 25;
        this.viewHeight = 20;
        this.steps = 0;
        this.visited = new Set([0]);
        this.announced = new Set([0]);
        this.hyperbolicMode = true;
        this.curvature = -1;
    }
    
    hyperbolicDistance(x1, y1, x2, y2) {
        const dx = x2 - x1, dy = y2 - y1;
        const e = Math.sqrt(dx*dx + dy*dy);
        return 2 * Math.atanh(Math.min(0.99, e / 100));
    }
    
    coordsToShard(x, y) {
        const angle = Math.atan2(y, x);
        return Math.abs(Math.floor((angle + Math.PI) / (2 * Math.PI) * 71) % 71);
    }
    
    getTerrain(x, y) {
        const s = this.coordsToShard(x, y);
        const l = OSM_LOCATIONS[s];
        return l ? l.emoji : EMOJIS[s % 15];
    }
    
    getLocationInfo(s) {
        return OSM_LOCATIONS[s] || {
            name: `Shard ${s}`,
            emoji: EMOJIS[s % 15],
            nodes: s === 0 ? 0 : Math.floor(45e9 * (s + 1))
        };
    }
    
    renderMap() {
        const map = document.getElementById('map');
        map.innerHTML = '';
        const sx = this.playerX - Math.floor(this.viewWidth / 2);
        const sy = this.playerY - Math.floor(this.viewHeight / 2);
        
        for (let y = 0; y < this.viewHeight; y++) {
            for (let x = 0; x < this.viewWidth; x++) {
                const wx = sx + x, wy = sy + y;
                const tile = document.createElement('div');
                tile.className = 'tile';
                tile.style.left = x * 32 + 'px';
                tile.style.top = y * 32 + 'px';
                
                if (this.hyperbolicMode) {
                    const d = this.hyperbolicDistance(this.playerX, this.playerY, wx, wy);
                    tile.style.transform = `scale(${1 / (1 + d * 0.5)})`;
                }
                
                tile.textContent = this.getTerrain(wx, wy);
                const s = this.coordsToShard(wx, wy);
                if (s === 17) tile.classList.add('cusp');
                if (s === 23) tile.classList.add('consciousness');
                if (s === 59) tile.classList.add('memory');
                map.appendChild(tile);
            }
        }
        
        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.textContent = '🧙';
        avatar.style.left = Math.floor(this.viewWidth / 2) * 32 + 'px';
        avatar.style.top = Math.floor(this.viewHeight / 2) * 32 + 'px';
        map.appendChild(avatar);
    }
    
    updateUI() {
        const s = this.coordsToShard(this.playerX, this.playerY);
        const l = this.getLocationInfo(s);
        const d = this.hyperbolicDistance(0, 0, this.playerX, this.playerY);
        const a = Math.atan2(this.playerY, this.playerX) * 180 / Math.PI;
        
        document.getElementById('position').textContent = `${this.playerX}, ${this.playerY}`;
        document.getElementById('shard-id').textContent = `${s} - ${l.name}`;
        document.getElementById('node-count').textContent = l.nodes.toLocaleString();
        document.getElementById('topology').textContent = TENFOLD[s % 10];
        document.getElementById('steps').textContent = this.steps;
        document.getElementById('visited').textContent = `${this.visited.size}/71`;
        document.getElementById('distance').textContent = d.toFixed(2);
        document.getElementById('angle').textContent = a.toFixed(1) + '°';
        this.visited.add(s);
    }
    
    move(dx, dy) {
        this.playerX += dx;
        this.playerY += dy;
        this.steps++;
        
        const s = this.coordsToShard(this.playerX, this.playerY);
        const l = this.getLocationInfo(s);
        
        if (l.special === 'CUSP' && !this.foundCusp) {
            this.addQuestLog(`🐯 FOUND: ${l.name}!`);
            this.foundCusp = true;
        }
        if (l.special === 'CONSCIOUSNESS' && !this.foundConsciousness) {
            this.addQuestLog(`🧬 FOUND: ${l.name}!`);
            this.foundConsciousness = true;
        }
        if (l.special === 'MEMORY' && !this.foundMemory) {
            this.addQuestLog(`🌙 FOUND: ${l.name}!`);
            this.foundMemory = true;
        }
        
        if (OSM_LOCATIONS[s] && !this.announced.has(s)) {
            this.addQuestLog(`📍 ${l.emoji} ${l.name}`);
            this.announced.add(s);
        }
        
        this.renderMap();
        this.updateUI();
    }
    
    teleportToShard(s) {
        const angle = s / 71 * 2 * Math.PI;
        const radius = 10 + s;
        this.playerX = Math.floor(radius * Math.cos(angle));
        this.playerY = Math.floor(radius * Math.sin(angle));
        this.addQuestLog(`⚡ Teleported to Shard ${s}`);
        this.renderMap();
        this.updateUI();
    }
    
    addQuestLog(msg) {
        const log = document.getElementById('quest-log');
        const entry = document.createElement('div');
        entry.textContent = `[${this.steps}] ${msg}`;
        entry.style.color = '#0ff';
        log.appendChild(entry);
        log.scrollTop = log.scrollHeight;
    }
    
    showInfo() {
        const s = this.coordsToShard(this.playerX, this.playerY);
        const l = this.getLocationInfo(s);
        this.addQuestLog(`${l.emoji} ${l.name}: ${(l.nodes/1e9).toFixed(1)}B nodes, ${TENFOLD[s % 10]}`);
    }
    
    init() {
        this.renderMap();
        this.updateUI();
        this.addQuestLog('⚡ Quest begun! Walk the hyperbolic plane.');
        
        document.addEventListener('keydown', e => {
            if (e.key === 'ArrowUp' || e.key === 'w') this.move(0, -1);
            if (e.key === 'ArrowDown' || e.key === 's') this.move(0, 1);
            if (e.key === 'ArrowLeft' || e.key === 'a') this.move(-1, 0);
            if (e.key === 'ArrowRight' || e.key === 'd') this.move(1, 0);
            if (e.key === 'c') this.teleportToShard(17);
            if (e.key === 'l') this.teleportToShard(23);
            if (e.key === 'm') this.teleportToShard(59);
            if (e.key === ' ') { e.preventDefault(); this.showInfo(); }
            if (e.key === 'h') {
                this.hyperbolicMode = !this.hyperbolicMode;
                this.addQuestLog(`Geometry: ${this.hyperbolicMode ? 'Hyperbolic' : 'Euclidean'}`);
                this.renderMap();
            }
        });
    }
}

const quest = new MonsterQuest();
quest.init();
window.quest = quest;
