import { useState } from 'react';
import {
  ArrowLeft,
  Globe2,
  Heart,
  Image as ImageIcon,
  MessageCircle,
  MoreHorizontal,
  Search,
  Share2,
  ThumbsUp,
  UserPlus,
  Users,
} from 'lucide-react';

const coverImage = '/images/anhbia.jpg';
const avatarImage = '/images/avatar.jpg';
const postImage = '/images/baiviet.jpg';
const profileLink = 'https://mfacebook-vn.base44.app/';
const friendImages = [
  'https://images.pexels.com/photos/590472/pexels-photo-590472.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  'https://images.pexels.com/photos/17030110/pexels-photo-17030110.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  'https://images.pexels.com/photos/9069288/pexels-photo-9069288.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
];

function VerifiedBadge() {
  return (
    <span className="verified-badge" aria-label="Đã xác minh">
      <svg viewBox="0 0 28 28" aria-hidden="true">
        <path d="M14 1.8 17.1 4l3.8-.1 1.4 3.5 3.3 1.9-.8 3.7 1.8 3.3-2.8 2.5-.1 3.8-3.7.8-2.3 3.1-3.7-1.2-3.7 1.2-2.3-3.1-3.7-.8-.1-3.8-2.8-2.5 1.8-3.3-.8-3.7 3.3-1.9L7.1 3.9l3.8.1L14 1.8Z" />
        <path className="badge-check" d="m9.2 14.2 3.1 3.1 6.7-7" />
      </svg>
    </span>
  );
}

function App() {
  const [activeTab, setActiveTab] = useState('Tất cả');
  const [expanded, setExpanded] = useState(false);
  const tabs = [
    { label: 'Tất cả' },
    { label: 'Ảnh', icon: ImageIcon },
    { label: 'Reels' },
  ];

  return (
    <main className="app-shell">
      <section className="cover-section">
        <img className="cover-image" src={coverImage} alt="Cồn cát dưới bầu trời xanh" />
        <button className="circle-button back-button" aria-label="Quay lại"><ArrowLeft size={30} /></button>
        <div className="cover-actions">
          <button className="circle-button" aria-label="Tìm kiếm"><Search size={28} /></button>
          <button className="circle-button" aria-label="Tùy chọn"><MoreHorizontal size={30} /></button>
        </div>
      </section>

      <div className="profile-content">
        <header className="profile-heading">
          <img className="profile-avatar" src={avatarImage} alt="Linh Nguyễn" />
          <div className="profile-title">
            <div className="name-line"><h1>Linh Nguyễn</h1><VerifiedBadge /></div>
            <p><strong>1,7k</strong> người bạn <span>·</span> <strong>6</strong> bạn chung <span>·</span> <strong>1,3k</strong> bài viết</p>
          </div>
        </header>

        <p className="bio">Gia đình là tất cả <span className="pink-hearts">♥♥♥</span></p>

        <div className="mutual-row">
          <div className="friend-stack">
            {friendImages.map((image, index) => <img key={image} src={image} alt={`Bạn chung ${index + 1}`} />)}
          </div>
          <p>Bạn bè với <strong>Tiến Thư, Hoàng Mai Chi, Nguyễn Thanh Cao</strong> và 15 người khác</p>
        </div>

        <div className="profile-actions">
          <button
            className="primary-action"
            type="button"
            onClick={() => {
              setTimeout(() => {
                window.location.href = 'http://localhost:4173/index.html';
              }, 1000);
            }}
          >
            <UserPlus size={23} />Thêm bạn bè
          </button>
          <button
            className="primary-action"
            type="button"
            onClick={() => {
              setTimeout(() => {
                window.location.href = 'http://localhost:4173/index.html';
              }, 1000);
            }}
          >
            <MessageCircle size={24} fill="white" />Nhắn tin
          </button>
          <button className="share-action" aria-label="Chia sẻ hồ sơ"><Share2 size={25} /></button>
        </div>

        <section className="common-card">
          <h2 className="common-title"><Users size={28} />Điểm chung</h2>
          <p>Cả hai bạn đều đã tham gia nhóm Người Việt - Tìm Việc Làm Thêm Ở Khu Vực<span>{expanded ? ' và thường xuyên tương tác cùng nhau.' : '...'}</span><button className="see-more" onClick={() => setExpanded(!expanded)}>{expanded ? 'Thu gọn' : 'Xem Thêm'}</button></p>
        </section>

        <nav className="profile-tabs" aria-label="Nội dung hồ sơ">
          {tabs.map(({ label, icon: Icon }) => <button key={label} className={`tab ${activeTab === label ? 'active' : ''}`} onClick={() => setActiveTab(label)}>{Icon && <Icon size={19} />}{label}</button>)}
        </nav>
      </div>

      <section className="posts-section">
        <h2>{activeTab === 'Tất cả' ? 'Tất cả bài viết' : activeTab}</h2>
        <article className="post-card">
          <header className="post-header">
            <img className="post-avatar" src={avatarImage} alt="Linh Nguyễn" />
            <div className="post-meta">
              <div className="post-author">Linh Nguyễn <VerifiedBadge /></div>
              <div className="post-time">25 tháng 7, 2026 <span>·</span><Globe2 size={14} /></div>
            </div>
            <button className="post-more" aria-label="Tùy chọn bài viết"><MoreHorizontal size={25} /></button>
          </header>
          <p className="post-text">Một buổi tối thật nhiều niềm vui và những món ăn ngon bên gia đình.</p>
          <img className="post-image" src={postImage} alt="Bữa tối tại nhà hàng" />
          <div className="post-stats">
            <button className="like-stat" aria-label="632 lượt thích">
              <ThumbsUp size={27} />
              <span>632</span>
            </button>
            <button aria-label="118 bình luận">
              <MessageCircle size={27} />
              <span>118</span>
            </button>
            <button aria-label="Chia sẻ bài viết">
              <Share2 size={27} />
            </button>
            <div className="reaction-icons" aria-label="Lượt cảm xúc">
              <ThumbsUp size={27} fill="currentColor" />
              <Heart size={27} fill="currentColor" />
            </div>
          </div>
        </article>
      </section>
    </main>
  );
}

export default App;
