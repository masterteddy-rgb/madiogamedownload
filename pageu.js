const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Constants
const SCREEN_WIDTH = 800;
const SCREEN_HEIGHT = 600;
const GRAVITY = 0.8;
const JUMP_POWER = -18;
const PLAYER_SPEED = 5;
const DODGE_DURATION = 10; // seconds
const DODGE_COOLDOWN = 60; // seconds

// Colors
const WHITE = "#FFFFFF";
const BLUE = "#0000FF";
const RED = "#FF0000";
const GREEN = "#00FF00";
const YELLOW = "#FFFF00";
const BLACK = "#000000";
const SAND = "#F5DEB3";
const GRAY = "#808080";
const BROWN = "#8B4513";

// Player
let player = {
    x: 100,
    y: SCREEN_HEIGHT - 72 - 50,
    width: 48,
    height: 72,
    widthGoku: 72,
    velX: 0,
    velY: 0,
    isJumping: false,
    level: 0,
    coins: 0,
    diamonds: 0
};

// Skins (replace src with your hosted image paths)
const skins = {
    "Mario": { image: null, unlocked: true, equipped: true, cost: 0 },
    "Luigi": { image: null, unlocked: false, equipped: false, cost: 1000 },
    "Peach": { image: null, unlocked: false, equipped: false, cost: 5000 },
    "Mushroom": { image: null, unlocked: false, equipped: false, cost: 10000 },
    "Steve": { image: null, unlocked: false, equipped: false, cost: 50000 },
    "Goku": { image: null, specialImage: null, unlocked: false, equipped: false, cost: 1000 },
    "Serious Saitama": { image: null, specialImage: null, unlocked: false, equipped: false, cost: 1500 }
};

// Load images (uncomment and adjust paths when hosted)
// Object.keys(skins).forEach(skin => {
//     skins[skin].image = new Image();
//     skins[skin].image.src = `${skin.toLowerCase()}.png`;
//     if (skin === "Goku" || skin === "Serious Saitama") {
//         skins[skin].specialImage = new Image();
//         skins[skin].specialImage.src = `${skin.toLowerCase()}_special.png`;
//     }
// });

// Levels
const levels = [
    {
        worldWidth: 2000,
        platforms: [{ x: 0, y: SCREEN_HEIGHT - 50, width: 2000, height: 50 }, { x: 300, y: 400, width: 200, height: 20 }, { x: 700, y: 350, width: 200, height: 20 }, { x: 1200, y: 300, width: 200, height: 20 }],
        pipes: [{ x: 500, y: SCREEN_HEIGHT - 100, width: 50, height: 50 }, { x: 900, y: SCREEN_HEIGHT - 150, width: 50, height: 100 }],
        monsters: [{ x: 600, y: SCREEN_HEIGHT - 98, velX: -2, width: 48, height: 48 }, { x: 1000, y: SCREEN_HEIGHT - 98, velX: -2, width: 48, height: 48 }],
        flag: { x: 1950, y: SCREEN_HEIGHT - 100, width: 20, height: 50 },
        coins: [{ x: 350, y: 350, width: 20, height: 20, collected: false }, { x: 750, y: 300, width: 20, height: 20, collected: false }, { x: 1250, y: 250, width: 20, height: 20, collected: false }],
        bgColor: WHITE
    },
    {
        worldWidth: 3000,
        platforms: [{ x: 0, y: SCREEN_HEIGHT - 50, width: 3000, height: 50 }, { x: 300, y: 450, width: 150, height: 20 }, { x: 600, y: 400, width: 200, height: 20 }, { x: 1000, y: 350, width: 200, height: 20 }, { x: 1500, y: 300, width: 200, height: 20 }, { x: 2000, y: 250, width: 200, height: 20 }],
        pipes: [{ x: 400, y: SCREEN_HEIGHT - 150, width: 50, height: 100 }, { x: 800, y: SCREEN_HEIGHT - 200, width: 50, height: 150 }, { x: 1300, y: SCREEN_HEIGHT - 100, width: 50, height: 50 }, { x: 1800, y: SCREEN_HEIGHT - 150, width: 50, height: 100 }],
        monsters: [{ x: 500, y: SCREEN_HEIGHT - 98, velX: -3, width: 48, height: 48 }, { x: 900, y: SCREEN_HEIGHT - 98, velX: -3, width: 48, height: 48 }, { x: 1400, y: SCREEN_HEIGHT - 98, velX: -3, width: 48, height: 48 }, { x: 1900, y: SCREEN_HEIGHT - 98, velX: -3, width: 48, height: 48 }],
        flag: { x: 2950, y: SCREEN_HEIGHT - 100, width: 20, height: 50 },
        coins: [{ x: 350, y: 400, width: 20, height: 20, collected: false }, { x: 650, y: 350, width: 20, height: 20, collected: false }, { x: 1050, y: 300, width: 20, height: 20, collected: false }, { x: 1550, y: 250, width: 20, height: 20, collected: false }, { x: 2050, y: 200, width: 20, height: 20, collected: false }],
        bgColor: WHITE
    },
    {
        worldWidth: 4000,
        platforms: [{ x: 0, y: SCREEN_HEIGHT - 50, width: 4000, height: 50 }, { x: 300, y: 450, width: 100, height: 20 }, { x: 600, y: 400, width: 150, height: 20 }, { x: 900, y: 350, width: 200, height: 20 }, { x: 1300, y: 300, width: 150, height: 20 }, { x: 1700, y: 250, width: 200, height: 20 }, { x: 2200, y: 200, width: 150, height: 20 }, { x: 2700, y: 150, width: 200, height: 20 }],
        pipes: [{ x: 400, y: SCREEN_HEIGHT - 200, width: 50, height: 150 }, { x: 800, y: SCREEN_HEIGHT - 250, width: 50, height: 200 }, { x: 1200, y: SCREEN_HEIGHT - 150, width: 50, height: 100 }, { x: 1600, y: SCREEN_HEIGHT - 200, width: 50, height: 150 }, { x: 2000, y: SCREEN_HEIGHT - 250, width: 50, height: 200 }, { x: 2500, y: SCREEN_HEIGHT - 150, width: 50, height: 100 }],
        monsters: [{ x: 500, y: SCREEN_HEIGHT - 98, velX: -4, width: 48, height: 48 }, { x: 800, y: SCREEN_HEIGHT - 98, velX: -4, width: 48, height: 48 }, { x: 1100, y: SCREEN_HEIGHT - 98, velX: -4, width: 48, height: 48 }, { x: 1500, y: SCREEN_HEIGHT - 98, velX: -4, width: 48, height: 48 }, { x: 2000, y: SCREEN_HEIGHT - 98, velX: -4, width: 48, height: 48 }, { x: 2500, y: SCREEN_HEIGHT - 98, velX: -4, width: 48, height: 48 }],
        flag: { x: 3950, y: SCREEN_HEIGHT - 100, width: 20, height: 50 },
        coins: [{ x: 350, y: 400, width: 20, height: 20, collected: false }, { x: 650, y: 350, width: 20, height: 20, collected: false }, { x: 950, y: 300, width: 20, height: 20, collected: false }, { x: 1350, y: 250, width: 20, height: 20, collected: false }, { x: 1750, y: 200, width: 20, height: 20, collected: false }, { x: 2250, y: 150, width: 20, height: 20, collected: false }, { x: 2750, y: 100, width: 20, height: 20, collected: false }],
        bgColor: WHITE
    },
    {
        worldWidth: 6000,
        platforms: [{ x: 0, y: SCREEN_HEIGHT - 50, width: 6000, height: 50 }, { x: 500, y: 450, width: 200, height: 20 }, { x: 1000, y: 400, width: 250, height: 20 }, { x: 1500, y: 350, width: 200, height: 20 }, { x: 2000, y: 300, width: 250, height: 20 }, { x: 2500, y: 250, width: 200, height: 20 }, { x: 3000, y: 200, width: 250, height: 20 }, { x: 3500, y: 250, width: 200, height: 20 }, { x: 4000, y: 300, width: 250, height: 20 }, { x: 4500, y: 350, width: 200, height: 20 }],
        pipes: [{ x: 600, y: SCREEN_HEIGHT - 200, width: 50, height: 150 }, { x: 1200, y: SCREEN_HEIGHT - 250, width: 50, height: 200 }, { x: 1800, y: SCREEN_HEIGHT - 150, width: 50, height: 100 }, { x: 2400, y: SCREEN_HEIGHT - 200, width: 50, height: 150 }, { x: 3000, y: SCREEN_HEIGHT - 250, width: 50, height: 200 }, { x: 3600, y: SCREEN_HEIGHT - 150, width: 50, height: 100 }, { x: 4200, y: SCREEN_HEIGHT - 200, width: 50, height: 150 }],
        monsters: [],
        boss: { x: 1000, y: SCREEN_HEIGHT - 200, width: 200, height: 200, velX: -5, bulletTimer: 0 },
        bullets: [],
        flag: { x: 5950, y: SCREEN_HEIGHT - 100, width: 20, height: 50 },
        coins: [{ x: 550, y: 400, width: 20, height: 20, collected: false }, { x: 1050, y: 350, width: 20, height: 20, collected: false }, { x: 1550, y: 300, width: 20, height: 20, collected: false }, { x: 2050, y: 250, width: 20, height: 20, collected: false }, { x: 2550, y: 200, width: 20, height: 20, collected: false }, { x: 3050, y: 150, width: 20, height: 20, collected: false }, { x: 3550, y: 200, width: 20, height: 20, collected: false }, { x: 4050, y: 250, width: 20, height: 20, collected: false }, { x: 4550, y: 300, width: 20, height: 20, collected: false }],
        bgColor: SAND
    }
];

// Game state
let gameState = "START_SCREEN"; // "START_SCREEN", "SKINS_MENU", "PLAYING", "DEAD", "WIN"
let currentLevel = 0;
let cameraX = 0;
let dodgeActive = false;
let dodgeStartTime = 0;
let lastDodgeTime = -DODGE_COOLDOWN * 1000;
let dodgeAnimationTime = 0;
const COIN_REWARDS = [500, 1000, 5000, 10000];
const LEVEL_INCREASE = [10, 30, 50, 100];
const DIAMOND_REWARD = 500;

// Controls
const leftBtn = document.getElementById("leftBtn");
const rightBtn = document.getElementById("rightBtn");
const jumpBtn = document.getElementById("jumpBtn");
const dodgeBtn = document.getElementById("dodgeBtn");

let leftPressed = false;
let rightPressed = false;

leftBtn.addEventListener("mousedown", () => leftPressed = true);
leftBtn.addEventListener("mouseup", () => leftPressed = false);
leftBtn.addEventListener("touchstart", () => leftPressed = true);
leftBtn.addEventListener("touchend", () => leftPressed = false);

rightBtn.addEventListener("mousedown", () => rightPressed = true);
rightBtn.addEventListener("mouseup", () => rightPressed = false);
rightBtn.addEventListener("touchstart", () => rightPressed = true);
rightBtn.addEventListener("touchend", () => rightPressed = false);

jumpBtn.addEventListener("mousedown", () => jump());
jumpBtn.addEventListener("touchstart", () => jump());

dodgeBtn.addEventListener("mousedown", () => dodge());
dodgeBtn.addEventListener("touchstart", () => dodge());

canvas.addEventListener("click", handleClick);

function jump() {
    if (!player.isJumping) {
        player.velY = JUMP_POWER;
        player.isJumping = true;
    }
}

function dodge() {
    const equippedSkin = Object.keys(skins).find(s => skins[s].equipped);
    if ((equippedSkin === "Goku" || equippedSkin === "Serious Saitama") && Date.now() - lastDodgeTime >= DODGE_COOLDOWN * 1000) {
        dodgeActive = true;
        dodgeStartTime = Date.now();
        lastDodgeTime = Date.now();
        dodgeAnimationTime = 0;
    }
}

function resetGame(level) {
    player.x = 100;
    player.y = SCREEN_HEIGHT - player.height - 50;
    player.velX = 0;
    player.velY = 0;
    player.isJumping = false;
    cameraX = 0;
    dodgeActive = false;
    dodgeAnimationTime = 0;
    gameState = "PLAYING";
    currentLevel = level;
    levels[level].coins.forEach(coin => coin.collected = false);
    levels[level].monsters.forEach(m => m.x = Math.random() * (levels[level].worldWidth - 600) + 600);
    if (levels[level].boss) {
        levels[level].boss.x = 1000;
        levels[level].bullets = [];
    }
}

function collides(rect1, rect2) {
    return rect1.x < rect2.x + rect2.width &&
           rect1.x + rect1.width > rect2.x &&
           rect1.y < rect2.y + rect2.height &&
           rect1.y + rect1.height > rect2.y;
}

function drawCharacter(x, y, skinName) {
    const width = skinName === "Goku" || skinName === "Serious Saitama" ? player.widthGoku : player.width;
    if (dodgeActive && (skinName === "Goku" || skinName === "Serious Saitama")) {
        const offsetX = Math.sin(dodgeAnimationTime * 15) * 8;
        const offsetY = Math.abs(Math.cos(dodgeAnimationTime * 10)) * 5;
        ctx.fillStyle = skinName === "Goku" ? "#FFA500" : "#FFD700"; // Orange for Goku, Gold for Saitama
        ctx.fillRect(x + offsetX - cameraX, y - offsetY, width, player.height);
    } else {
        ctx.fillStyle = skinName === "Mario" ? RED : skinName === "Luigi" ? GREEN : skinName === "Peach" ? "#FFC1CC" : skinName === "Mushroom" ? BROWN : skinName === "Steve" ? "#00CED1" : "#FFA500";
        ctx.fillRect(x - cameraX, y, width, player.height);
    }
    return width;
}

function drawGoomba(monster) {
    const x = monster.x - cameraX;
    ctx.fillStyle = BROWN;
    ctx.fillRect(x + 6, monster.y, 36, 24);
    ctx.fillStyle = BLACK;
    ctx.fillRect(x, monster.y + 24, 48, 12);
    ctx.fillStyle = WHITE;
    ctx.fillRect(x + 12, monster.y + 6, 6, 6);
    ctx.fillRect(x + 30, monster.y + 6, 6, 6);
    ctx.fillStyle = BLACK;
    ctx.fillRect(x + 15, monster.y + 9, 3, 3);
    ctx.fillRect(x + 33, monster.y + 9, 3, 3);
}

function drawBoss(boss) {
    ctx.fillStyle = RED;
    ctx.fillRect(boss.x - cameraX, boss.y, boss.width, boss.height);
    ctx.fillStyle = BLACK;
    ctx.beginPath();
    ctx.arc(boss.x - cameraX + 50, boss.y + 50, 20, 0, Math.PI * 2);
    ctx.arc(boss.x - cameraX + 150, boss.y + 50, 20, 0, Math.PI * 2);
    ctx.fill();
}

function drawBullets(bullets) {
    bullets.forEach(bullet => {
        ctx.fillStyle = BLACK;
        ctx.beginPath();
        ctx.arc(bullet.x - cameraX, bullet.y, 10, 0, Math.PI * 2);
        ctx.fill();
    });
}

function drawProgressBar() {
    const barWidth = SCREEN_WIDTH - 40;
    ctx.strokeStyle = BLACK;
    ctx.lineWidth = 2;
    ctx.strokeRect(20, 20, barWidth, 20);
    const playerPos = (player.x / levels[currentLevel].worldWidth) * barWidth + 20;
    ctx.fillStyle = RED;
    ctx.beginPath();
    ctx.arc(playerPos, 30, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = YELLOW;
    ctx.beginPath();
    ctx.arc(barWidth + 20, 30, 5, 0, Math.PI * 2);
    ctx.fill();
}

function handleClick(event) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    if (gameState === "START_SCREEN") {
        if (x > 350 && x < 550) {
            if (y > 250 && y < 290) resetGame(0);
            else if (y > 290 && y < 330) resetGame(1);
            else if (y > 330 && y < 370) resetGame(2);
            else if (y > 370 && y < 410 && player.level >= 500) resetGame(3);
            else if (y > 410 && y < 450) gameState = "SKINS_MENU";
        }
    } else if (gameState === "SKINS_MENU") {
        if (x > 50 && x < 250) {
            if (y > 150 && y < 190 && skins["Mario"].unlocked) equipSkin("Mario");
            else if (y > 210 && y < 250) buyOrEquip("Luigi");
            else if (y > 270 && y < 310) buyOrEquip("Peach");
            else if (y > 330 && y < 370) buyOrEquip("Mushroom");
            else if (y > 390 && y < 430) buyOrEquip("Steve");
            else if (y > 450 && y < 490) buyOrEquip("Goku");
            else if (y > 510 && y < 550) buyOrEquip("Serious Saitama");
        }
        if (x > 350 && x < 550 && y > 550 && y < 590) gameState = "START_SCREEN";
    } else if (gameState === "DEAD" || gameState === "WIN") {
        if (x > 350 && x < 650 && y > 350 && y < 390) {
            if (gameState === "WIN") {
                player.coins += COIN_REWARDS[currentLevel];
                player.level += LEVEL_INCREASE[currentLevel];
                if (currentLevel === 3) player.diamonds += DIAMOND_REWARD;
            }
            resetGame(currentLevel);
        }
    }
}

function equipSkin(skin) {
    Object.keys(skins).forEach(s => skins[s].equipped = false);
    skins[skin].equipped = true;
}

function buyOrEquip(skin) {
    if (skins[skin].unlocked) {
        equipSkin(skin);
    } else if ((skin === "Goku" || skin === "Serious Saitama") && player.diamonds >= skins[skin].cost) {
        skins[skin].unlocked = true;
        player.diamonds -= skins[skin].cost;
    } else if (player.coins >= skins[skin].cost) {
        skins[skin].unlocked = true;
        player.coins -= skins[skin].cost;
    }
}

function update() {
    const now = Date.now();
    if (dodgeActive && (now - dodgeStartTime) / 1000 >= DODGE_DURATION) dodgeActive = false;
    if (dodgeActive) dodgeAnimationTime += 1 / 60;

    player.velX = leftPressed ? -PLAYER_SPEED : rightPressed ? PLAYER_SPEED : 0;
    player.x += player.velX;
    player.y += player.velY;
    player.velY += GRAVITY;

    if (player.x - cameraX > SCREEN_WIDTH * 0.7) cameraX = player.x - SCREEN_WIDTH * 0.7;
    if (cameraX < 0) cameraX = 0;
    if (cameraX > levels[currentLevel].worldWidth - SCREEN_WIDTH) cameraX = levels[currentLevel].worldWidth - SCREEN_WIDTH;

    const equippedSkin = Object.keys(skins).find(s => skins[s].equipped) || "Mario";
    const currentWidth = drawCharacter(player.x, player.y, equippedSkin);
    const playerRect = { x: player.x, y: player.y, width: currentWidth, height: player.height };

    for (let platform of levels[currentLevel].platforms) {
        if (collides(playerRect, platform)) {
            if (player.velY > 0) {
                player.y = platform.y - player.height;
                player.velY = 0;
                player.isJumping = false;
            }
        }
    }

    for (let pipe of levels[currentLevel].pipes) {
        if (collides(playerRect, pipe)) {
            if (player.velX > 0) player.x = pipe.x - currentWidth;
            else if (player.velX < 0) player.x = pipe.x + pipe.width;
        }
    }

    levels[currentLevel].coins = levels[currentLevel].coins.filter(coin => {
        if (!coin.collected && collides(playerRect, coin)) {
            player.coins += 50;
            return false;
        }
        return true;
    });

    for (let monster of levels[currentLevel].monsters) {
        monster.x += monster.velX;
        if (monster.x < 0 || monster.x > levels[currentLevel].worldWidth - monster.width) monster.velX *= -1;
        if (collides(playerRect, monster) && !dodgeActive) gameState = "DEAD";
    }

    if (levels[currentLevel].boss) {
        const boss = levels[currentLevel].boss;
        boss.x += boss.velX;
        if (boss.x < player.x - 500 || boss.x > player.x + 500) boss.velX *= -1;
        if (collides(playerRect, boss) && !dodgeActive) gameState = "DEAD";
        boss.bulletTimer++;
        if (boss.bulletTimer >= 60) {
            levels[currentLevel].bullets.push({ x: boss.x, y: boss.y + boss.height / 2, velX: -10 });
            boss.bulletTimer = 0;
        }
        levels[currentLevel].bullets = levels[currentLevel].bullets.filter(bullet => {
            bullet.x += bullet.velX;
            if (collides(playerRect, { x: bullet.x, y: bullet.y - 5, width: 20, height: 20 }) && !dodgeActive) {
                gameState = "DEAD";
                return false;
            }
            return bullet.x > 0;
        });
    }

    if (collides(playerRect, levels[currentLevel].flag)) gameState = "WIN";

    if (player.x < 0) player.x = 0;
    if (player.y > SCREEN_HEIGHT - player.height) {
        player.y = SCREEN_HEIGHT - player.height;
        player.velY = 0;
        player.isJumping = false;
    }
}

function draw() {
    ctx.fillStyle = levels[currentLevel].bgColor || BLACK;
    ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);

    if (gameState === "START_SCREEN") {
        ctx.fillStyle = WHITE;
        ctx.font = "40px Arial";
        ctx.fillText("MarioCraft", 375, 100);
        ctx.fillStyle = YELLOW;
        ctx.fillText(`Coins: ${player.coins}`, 375, 150);
        ctx.fillStyle = "#00BFFF";
        ctx.fillText(`Diamonds: ${player.diamonds}`, 375, 180);
        ctx.fillStyle = WHITE;
        ctx.fillText(`Level: ${player.level}`, 375, 210);
        ctx.font = "20px Arial";
        ctx.fillText("Tap for Level 1 (Easy)", 350, 270);
        ctx.fillText("Tap for Level 2 (Medium)", 350, 310);
        ctx.fillText("Tap for Level 3 (Hard)", 350, 350);
        ctx.fillStyle = player.level >= 500 ? WHITE : GRAY;
        ctx.fillText("Tap for Level 4 (Hell) [500+]", 350, 390);
        ctx.fillStyle = WHITE;
        ctx.fillText("Tap for Skins", 375, 430);
    } else if (gameState === "SKINS_MENU") {
        ctx.fillStyle = WHITE;
        ctx.font = "40px Arial";
        ctx.fillText("Skins Menu", 375, 50);
        ctx.fillStyle = YELLOW;
        ctx.fillText(`Coins: ${player.coins}`, 375, 100);
        ctx.fillStyle = "#00BFFF";
        ctx.fillText(`Diamonds: ${player.diamonds}`, 375, 130);
        ctx.font = "20px Arial";
        ctx.fillStyle = WHITE;
        ctx.fillText(`Mario (${skins["Mario"].equipped ? "Equipped" : "Unequipped"})`, 50, 170);
        ctx.fillText(`Luigi (${skins["Luigi"].equipped ? "Equipped" : "Unequipped"})`, 50, 230);
        if (!skins["Luigi"].unlocked) ctx.fillStyle = YELLOW, ctx.fillText(`Cost: ${skins["Luigi"].cost} Coins`, 50, 200);
        ctx.fillStyle = WHITE;
        ctx.fillText(`Peach (${skins["Peach"].equipped ? "Equipped" : "Unequipped"})`, 50, 290);
        if (!skins["Peach"].unlocked) ctx.fillStyle = YELLOW, ctx.fillText(`Cost: ${skins["Peach"].cost} Coins`, 50, 260);
        ctx.fillStyle = WHITE;
        ctx.fillText(`Mushroom (${skins["Mushroom"].equipped ? "Equipped" : "Unequipped"})`, 50, 350);
        if (!skins["Mushroom"].unlocked) ctx.fillStyle = YELLOW, ctx.fillText(`Cost: ${skins["Mushroom"].cost} Coins`, 50, 320);
        ctx.fillStyle = WHITE;
        ctx.fillText(`Steve (${skins["Steve"].equipped ? "Equipped" : "Unequipped"})`, 50, 410);
        if (!skins["Steve"].unlocked) ctx.fillStyle = YELLOW, ctx.fillText(`Cost: ${skins["Steve"].cost} Coins`, 50, 380);
        ctx.fillStyle = WHITE;
        ctx.fillText(`Goku (${skins["Goku"].equipped ? "Equipped" : "Unequipped"})`, 50, 470);
        if (!skins["Goku"].unlocked) ctx.fillStyle = "#00BFFF", ctx.fillText(`Cost: ${skins["Goku"].cost} Diamonds`, 50, 440);
        ctx.fillStyle = WHITE;
        ctx.fillText(`S. Saitama (${skins["Serious Saitama"].equipped ? "Equipped" : "Unequipped"})`, 50, 530);
        if (!skins["Serious Saitama"].unlocked) ctx.fillStyle = "#00BFFF", ctx.fillText(`Cost: ${skins["Serious Saitama"].cost} Diamonds`, 50, 500);
        ctx.fillStyle = WHITE;
        ctx.fillText("Tap to return", 350, 570);
    } else if (gameState === "PLAYING") {
        ctx.fillStyle = BLUE;
        levels[currentLevel].platforms.forEach(p => ctx.fillRect(p.x - cameraX, p.y, p.width, p.height));
        ctx.fillStyle = GREEN;
        levels[currentLevel].pipes.forEach(p => ctx.fillRect(p.x - cameraX, p.y, p.width, p.height));
        ctx.fillStyle = YELLOW;
        levels[currentLevel].coins.forEach(c => !c.collected && ctx.fillRect(c.x - cameraX, c.y, c.width, c.height));
        levels[currentLevel].monsters.forEach(drawGoomba);
        if (levels[currentLevel].boss) {
            drawBoss(levels[currentLevel].boss);
            drawBullets(levels[currentLevel].bullets);
        }
        drawCharacter(player.x, player.y, Object.keys(skins).find(s => skins[s].equipped) || "Mario");
        ctx.fillStyle = YELLOW;
        ctx.fillRect(levels[currentLevel].flag.x - cameraX, levels[currentLevel].flag.y, 20, 50);
        drawProgressBar();
        ctx.fillStyle = WHITE;
        ctx.font = "20px Arial";
        ctx.fillText(`Coins: ${player.coins}`, 10, 30);
        const equippedSkin = Object.keys(skins).find(s => skins[s].equipped);
        if (equippedSkin === "Goku" || equippedSkin === "Serious Saitama") {
            const cooldown = Math.max(0, DODGE_COOLDOWN - (Date.now() - lastDodgeTime) / 1000);
            ctx.fillStyle = cooldown === 0 ? WHITE : GRAY;
            ctx.fillText(`Dodge: ${Math.ceil(cooldown)}s`, 10, 50);
        }
    } else if (gameState === "DEAD") {
        ctx.fillStyle = RED;
        ctx.font = "40px Arial";
        ctx.fillText("You Died! Tap to Restart", 250, 320);
    } else if (gameState === "WIN") {
        ctx.fillStyle = GREEN;
        ctx.font = "40px Arial";
        ctx.fillText(`Level ${currentLevel + 1} Complete! Tap to Restart`, 200, 320);
    }
}

function gameLoop() {
    if (gameState === "PLAYING") update();
    draw();
    requestAnimationFrame(gameLoop);
}

gameLoop();