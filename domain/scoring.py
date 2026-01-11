def calculate_scores(spots_df, user_tags):
    """
    ユーザーの回答タグに基づいて各スポットのスコアを計算する
    """
    scores = {}
    
    for index, row in spots_df.iterrows():
        spot_id = row['No']
        spot_keywords = row['keywords_list']
        
        score = 0
        for tag in user_tags:
            if tag in spot_keywords:
                score += 1
        
        scores[spot_id] = score
        
    return scores

def recommend_spot(spots_df, user_tags):
    """
    スコアに基づいて推奨スポットを決定する
    ユーザーが「未知の一歩」タグを選んでいる場合、あえて1位ではなく2位や3位を提案するロジックを入れる
    """
    if spots_df.empty:
        return None

    scores = calculate_scores(spots_df, user_tags)
    
    # スコアで降順ソート
    sorted_spots = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # 未知の一歩ロジック
    is_adventure = "未知の一歩" in user_tags
    
    if is_adventure and len(sorted_spots) >= 2:
        # 1位ではなく2位を返す（候補があれば）
        # ただし、スコアが0の場合は除外したいが、簡易実装としてそのまま返す
        recommended_spot_id = sorted_spots[1][0]
    else:
        # 通常は1位を返す
        recommended_spot_id = sorted_spots[0][0]
        
    return recommended_spot_id
