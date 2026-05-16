function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return '';
}

async function apiFetch(url, options = {}) {
  const response = await fetch(url, {
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(JSON.stringify(error));
  }

  if (response.status === 204) return null;
  return response.json();
}

function showCartToast(text) {
  const toast = document.querySelector('[data-cart-toast]');
  if (!toast) return;
  toast.textContent = text;
  toast.classList.add('is-visible');
  clearTimeout(showCartToast.timer);
  showCartToast.timer = setTimeout(() => toast.classList.remove('is-visible'), 2200);
}

async function updateCartCount() {
  try {
    const cart = await apiFetch('/api/cart/');
    document.querySelectorAll('[data-cart-count]').forEach((node) => {
      node.textContent = cart.total_quantity || 0;
    });
    return cart;
  } catch {
    return null;
  }
}

function getCarouselStep(carousel) {
  const firstCard = carousel.querySelector(':scope > *');
  const styles = getComputedStyle(carousel);
  const gap = parseFloat(styles.columnGap || styles.gap || 0);
  return firstCard ? firstCard.getBoundingClientRect().width + gap : carousel.clientWidth * 0.8;
}

function scrollCarousel(id, direction) {
  const carousel = document.getElementById(id);
  if (!carousel) return;
  const step = getCarouselStep(carousel);
  const maxScroll = Math.max(0, carousel.scrollWidth - carousel.clientWidth);

  if (direction < 0 && carousel.scrollLeft <= 8) {
    carousel.scrollTo({ left: maxScroll, behavior: 'smooth' });
    return;
  }

  if (direction > 0 && carousel.scrollLeft >= maxScroll - 8) {
    carousel.scrollTo({ left: 0, behavior: 'smooth' });
    return;
  }

  carousel.scrollBy({ left: direction * step, behavior: 'smooth' });
}

function initCarousels() {
  document.querySelectorAll('[data-carousel-prev]').forEach((button) => {
    button.addEventListener('click', () => scrollCarousel(button.dataset.carouselPrev, -1));
  });
  document.querySelectorAll('[data-carousel-next]').forEach((button) => {
    button.addEventListener('click', () => scrollCarousel(button.dataset.carouselNext, 1));
  });
}

function initHeroSlider() {
  const slides = Array.from(document.querySelectorAll('.hero-slide'));
  const dots = Array.from(document.querySelectorAll('.hero-slider__dots span'));
  const copies = Array.from(document.querySelectorAll('[data-hero-copy]'));
  let activeSlide = 0;

  function showHeroSlide(index) {
    activeSlide = index;
    slides.forEach((slide, slideIndex) => slide.classList.toggle('is-active', slideIndex === activeSlide));
    dots.forEach((dot, index) => dot.classList.toggle('is-active', index === activeSlide));
    copies.forEach((copy, copyIndex) => copy.classList.toggle('is-active', copyIndex === activeSlide));
  }

  showHeroSlide(0);
  if (slides.length <= 1) return;

  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => showHeroSlide(index));
  });

  setInterval(() => {
    showHeroSlide((activeSlide + 1) % slides.length);
  }, 5000);
}

function initProductDetail() {
  document.querySelectorAll('.product-thumbs button').forEach((button) => {
    button.addEventListener('click', () => {
      const main = document.querySelector('.product-main-photo');
      const img = button.querySelector('img');
      if (!main || !img) return;
      main.src = img.src;
      main.alt = img.alt;
      document.querySelectorAll('.product-thumbs button').forEach((item) => item.classList.remove('is-active'));
      button.classList.add('is-active');
    });
  });

  const orderButton = document.querySelector('.order-product-btn');
  const price = document.querySelector('[data-price]');
  const activeWeight = document.querySelector('.weight-options button.is-active');
  if (orderButton && activeWeight?.dataset.weightOptionId) {
    orderButton.dataset.weightOptionId = activeWeight.dataset.weightOptionId;
  }

  document.querySelectorAll('.weight-options button[data-weight-option-id]').forEach((button) => {
    button.addEventListener('click', () => {
      document.querySelectorAll('.weight-options button').forEach((item) => item.classList.remove('is-active'));
      button.classList.add('is-active');
      if (price && button.dataset.price) price.textContent = `${button.dataset.price} BYN`;
      if (orderButton) orderButton.dataset.weightOptionId = button.dataset.weightOptionId;
    });
  });

  document.querySelectorAll('.accordion-button').forEach((button) => {
    button.addEventListener('click', () => {
      button.closest('.accordion-item')?.classList.toggle('is-open');
    });
  });
}

async function addToCart(button) {
  const productId = button.dataset.productId;
  const weightOptionId = button.dataset.weightOptionId;
  if (!productId || !weightOptionId) return;

  await apiFetch('/api/cart/items/', {
    method: 'POST',
    body: JSON.stringify({
      product_id: productId,
      weight_option_id: weightOptionId,
      quantity: 1,
    }),
  });
  await updateCartCount();
  showCartToast('Товар добавлен в корзину');

  const oldText = button.textContent;
  button.classList.add('is-added');
  button.textContent = button.classList.contains('order-product-btn') ? 'Добавлено' : '✓';
  setTimeout(() => {
    button.classList.remove('is-added');
    button.textContent = oldText;
  }, 1100);
}

function initAddToCart() {
  document.querySelectorAll('.add-to-cart').forEach((button) => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      addToCart(button).catch(() => showCartToast('Не удалось добавить товар'));
    });
  });
}

function renderCart(cart) {
  const container = document.querySelector('[data-cart-items]');
  const totalNode = document.querySelector('[data-cart-total]');
  if (!container) return;

  if (totalNode) totalNode.textContent = `${Number(cart.total_price || 0).toFixed(0)} BYN`;

  if (!cart.items?.length) {
    container.innerHTML = `
      <div class="cart-empty">
        <h2>Корзина пустая</h2>
        <p>Добавьте торт или десерт из каталога, и он появится здесь.</p>
        <a href="/">Перейти в каталог</a>
      </div>
    `;
    return;
  }

  container.innerHTML = cart.items.map((item) => {
    const image = item.product.main_image_url || '/static/assets/product-cake.jpg';
    return `
      <article class="cart-item" data-cart-id="${item.id}">
        <a class="cart-item__image" href="${item.product.url}" aria-label="Перейти к товару ${item.product.title}">
          <img src="${image}" alt="${item.product.title}">
        </a>
        <div>
          <h3><a href="${item.product.url}">${item.product.title}</a></h3>
          <p>Вес: ${Number(item.weight_option.weight).toString()} кг</p>
          <div class="cart-item__controls">
            <button type="button" data-cart-minus="${item.id}">−</button>
            <strong>${item.quantity}</strong>
            <button type="button" data-cart-plus="${item.id}">+</button>
            <button class="cart-remove" type="button" data-cart-remove="${item.id}">Удалить</button>
          </div>
        </div>
        <div class="cart-item__price">${Number(item.line_total).toFixed(0)} BYN</div>
      </article>
    `;
  }).join('');
}

async function refreshCartPage() {
  const cart = await updateCartCount();
  if (cart) renderCart(cart);
}

function initCartPage() {
  if (!document.querySelector('[data-cart-items]')) return;
  refreshCartPage();

  document.addEventListener('click', async (event) => {
    const plus = event.target.closest('[data-cart-plus]');
    const minus = event.target.closest('[data-cart-minus]');
    const remove = event.target.closest('[data-cart-remove]');
    if (!plus && !minus && !remove) return;

    const id = plus?.dataset.cartPlus || minus?.dataset.cartMinus || remove?.dataset.cartRemove;
    const item = document.querySelector(`[data-cart-id="${id}"]`);
    const quantity = Number(item?.querySelector('.cart-item__controls strong')?.textContent || 1);

    try {
      if (remove || quantity <= 1 && minus) {
        await apiFetch(`/api/cart/items/${id}/`, { method: 'DELETE' });
      } else {
        await apiFetch(`/api/cart/items/${id}/`, {
          method: 'PATCH',
          body: JSON.stringify({ quantity: plus ? quantity + 1 : quantity - 1 }),
        });
      }
      await refreshCartPage();
    } catch {
      showCartToast('Не удалось обновить корзину');
    }
  });

  document.querySelector('[data-checkout]')?.addEventListener('click', async () => {
    const message = document.querySelector('[data-checkout-message]');
    const payload = {
      customer_name: document.querySelector('[data-order-name]')?.value || '',
      phone: document.querySelector('[data-order-phone]')?.value || '',
      event_date: document.querySelector('[data-order-date]')?.value || null,
      comment: document.querySelector('[data-order-comment]')?.value || '',
    };

    try {
      const order = await apiFetch('/api/orders/', { method: 'POST', body: JSON.stringify(payload) });
      if (message) message.textContent = `Заявка оформлена. Номер: ${order.public_id}`;
      await refreshCartPage();
    } catch {
      if (message) message.textContent = 'Проверьте телефон и наличие товаров в корзине.';
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initCarousels();
  initHeroSlider();
  initProductDetail();
  initAddToCart();
  initCartPage();
  updateCartCount();
});
